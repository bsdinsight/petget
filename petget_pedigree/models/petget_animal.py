import html

from odoo import api, fields, models

REGISTRY = [
    ('ankc', 'Dogs Australia (ANKC)'),
    ('saca', 'SA Canine Association'),
    ('dogsnsw', 'Dogs NSW (RNSWCC)'),
    ('dogsvic', 'Dogs Victoria (VCA)'),
    ('dogsqld', 'Dogs Queensland'),
    ('dogswest', 'Dogs West'),
    ('tca', 'Tasmanian Canine Association'),
    ('dogsnt', 'Dogs NT'),
    ('dogsact', 'Dogs ACT'),
    ('other', 'Other'),
]


class PetgetAnimal(models.Model):
    _inherit = 'petget.animal'

    registry_body = fields.Selection(REGISTRY, string='Registry Body')
    origin_country_id = fields.Many2one('res.country', string='Country of Origin')
    is_pedigree_only = fields.Boolean(
        string='Pedigree Reference Only',
        help='Ancestor kept only for pedigree records; hidden from the managed-animal list.',
    )
    pedigree_html = fields.Html(
        string='Pedigree', compute='_compute_pedigree_html', sanitize=False,
    )
    coi_percent = fields.Float(
        string='Inbreeding COI (%)', compute='_compute_coi', digits=(6, 2),
        help='Wright\'s Coefficient of Inbreeding, computed from the recorded '
             'pedigree. Accuracy depends on how many generations are on file.',
    )

    # ------------------------------------------------------------------
    # Classic pedigree grid (3 generations)
    # ------------------------------------------------------------------
    def _ancestor(self, path):
        """Walk sire/dam links following a path of 'S'/'D'."""
        animal = self
        for step in path:
            animal = animal.sire_id if step == 'S' else animal.dam_id
            if not animal:
                return self.browse()
        return animal

    @staticmethod
    def _ped_cell(animal, rowspan, kind):
        bg = '#eaf2fb' if kind == 'sire' else '#fdeef2'
        style = ('border:1px solid #cfd6dd;padding:6px 8px;background:%s;'
                 'vertical-align:middle;' % bg)
        if not animal:
            return ('<td rowspan="%d" style="%scolor:#9aa3ab;">—</td>'
                    % (rowspan, style))
        name = html.escape(animal.name or '?')
        reg = ''
        if animal.registration_number:
            reg = ('<div style="font-size:11px;color:#6b7280;">%s</div>'
                   % html.escape(animal.registration_number))
        return ('<td rowspan="%d" style="%s"><strong>%s</strong>%s</td>'
                % (rowspan, style, name, reg))

    @api.depends('sire_id', 'dam_id')
    def _compute_pedigree_html(self):
        for rec in self:
            if not rec.sire_id and not rec.dam_id:
                rec.pedigree_html = False
                continue
            c = lambda path, span, kind: rec._ped_cell(rec._ancestor(path), span, kind)
            rows = [
                '<tr>%s%s%s</tr>' % (c(['S'], 4, 'sire'), c(['S', 'S'], 2, 'sire'), c(['S', 'S', 'S'], 1, 'sire')),
                '<tr>%s</tr>' % c(['S', 'S', 'D'], 1, 'dam'),
                '<tr>%s%s</tr>' % (c(['S', 'D'], 2, 'dam'), c(['S', 'D', 'S'], 1, 'sire')),
                '<tr>%s</tr>' % c(['S', 'D', 'D'], 1, 'dam'),
                '<tr>%s%s%s</tr>' % (c(['D'], 4, 'dam'), c(['D', 'S'], 2, 'sire'), c(['D', 'S', 'S'], 1, 'sire')),
                '<tr>%s</tr>' % c(['D', 'S', 'D'], 1, 'dam'),
                '<tr>%s%s</tr>' % (c(['D', 'D'], 2, 'dam'), c(['D', 'D', 'S'], 1, 'sire')),
                '<tr>%s</tr>' % c(['D', 'D', 'D'], 1, 'dam'),
            ]
            rec.pedigree_html = (
                '<table style="border-collapse:collapse;width:100%%;'
                'font-size:13px;table-layout:fixed;">%s</table>' % ''.join(rows)
            )

    # ------------------------------------------------------------------
    # Coefficient of Inbreeding (Wright), via recursive kinship
    # ------------------------------------------------------------------
    def _generation(self, animal, memo):
        if not animal:
            return 0
        if animal.id in memo:
            return memo[animal.id]
        memo[animal.id] = 0  # cycle guard
        if not animal.sire_id and not animal.dam_id:
            g = 0
        else:
            g = 1 + max(self._generation(animal.sire_id, memo),
                        self._generation(animal.dam_id, memo))
        memo[animal.id] = g
        return g

    def _kinship(self, a, b, cache, gmemo):
        if not a or not b:
            return 0.0
        if a.id == b.id:
            key = ('self', a.id)
            if key in cache:
                return cache[key]
            f = 0.5 * (1.0 + self._kinship(a.sire_id, a.dam_id, cache, gmemo))
            cache[key] = f
            return f
        key = (min(a.id, b.id), max(a.id, b.id))
        if key in cache:
            return cache[key]
        # expand the more recent individual (higher generation number)
        if self._generation(a, gmemo) >= self._generation(b, gmemo):
            val = 0.5 * (self._kinship(a.sire_id, b, cache, gmemo)
                         + self._kinship(a.dam_id, b, cache, gmemo))
        else:
            val = 0.5 * (self._kinship(a, b.sire_id, cache, gmemo)
                         + self._kinship(a, b.dam_id, cache, gmemo))
        cache[key] = val
        return val

    @api.depends('sire_id', 'dam_id')
    def _compute_coi(self):
        for rec in self:
            if rec.sire_id and rec.dam_id:
                f = rec._kinship(rec.sire_id, rec.dam_id, {}, {})
            else:
                f = 0.0
            rec.coi_percent = round(f * 100.0, 2)
