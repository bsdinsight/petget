from odoo import _, api, fields, models


class PetgetMating(models.Model):
    _inherit = 'petget.mating'

    breeding_warning_html = fields.Html(
        string='Breeding Warnings', compute='_compute_breeding_warning',
        sanitize=False,
    )
    breeding_warning_count = fields.Integer(
        string='Breeding Warning Count', compute='_compute_breeding_warning',
    )

    @api.depends('dam_id', 'sire_id',
                 'dam_id.breeding_restricted', 'sire_id.breeding_restricted',
                 'dam_id.has_hip_elbow', 'sire_id.has_hip_elbow')
    def _compute_breeding_warning(self):
        for rec in self:
            warnings = []
            for role, animal in [(_('Dam'), rec.dam_id), (_('Sire'), rec.sire_id)]:
                if not animal:
                    continue
                if animal.breeding_restricted:
                    warnings.append(_(
                        '%(role)s "%(name)s" is marked Not for Breeding (Limited Register).',
                        role=role, name=animal.name,
                    ))
                if not animal.has_hip_elbow:
                    warnings.append(_(
                        '%(role)s "%(name)s" has no hip/elbow clearance on record.',
                        role=role, name=animal.name,
                    ))
            rec.breeding_warning_count = len(warnings)
            if warnings:
                items = ''.join('<li>%s</li>' % w for w in warnings)
                rec.breeding_warning_html = '<ul class="mb-0">%s</ul>' % items
            else:
                rec.breeding_warning_html = False
