from odoo import _, api, fields, models


class PetgetAnimal(models.Model):
    _inherit = 'petget.animal'

    dam_litter_ids = fields.One2many(
        'petget.litter', 'dam_id', string='Litters as Dam',
    )
    compliance_warning_html = fields.Html(
        string='Compliance Warnings', compute='_compute_compliance',
        sanitize=False,
    )
    compliance_warning_count = fields.Integer(
        string='Compliance Warning Count', compute='_compute_compliance',
    )

    def _get_compliance_rule(self):
        self.ensure_one()
        state = self.company_id.petget_au_state
        if not state:
            return self.env['petget.compliance.au.rule'].browse()
        species = self.species if self.species in ('dog', 'cat') else 'dog'
        return self.env['petget.compliance.au.rule'].search(
            [('state', '=', state), ('species', '=', species)], limit=1)

    @api.depends('date_of_birth', 'microchip', 'status', 'sex', 'species',
                 'company_id', 'company_id.petget_au_state', 'dam_litter_ids')
    def _compute_compliance(self):
        today = fields.Date.context_today(self)
        for rec in self:
            warnings = []
            rule = rec._get_compliance_rule()
            age_weeks = None
            if rec.date_of_birth and rec.date_of_birth <= today:
                age_weeks = (today - rec.date_of_birth).days // 7
            if rule:
                if (rule.min_sale_age_weeks and rec.status in ('sold', 'rehomed')
                        and age_weeks is not None
                        and age_weeks < rule.min_sale_age_weeks):
                    warnings.append(_(
                        'Marked %(status)s before the minimum sale age of '
                        '%(weeks)s weeks.',
                        status=rec.status, weeks=rule.min_sale_age_weeks,
                    ))
                if (rule.microchip_required_age_weeks and not rec.microchip
                        and age_weeks is not None
                        and age_weeks >= rule.microchip_required_age_weeks):
                    warnings.append(_(
                        'Microchip required by %(weeks)s weeks of age — '
                        'none recorded.',
                        weeks=rule.microchip_required_age_weeks,
                    ))
                if rec.sex == 'female' and rule.max_lifetime_litters:
                    n_litters = len(rec.dam_litter_ids)
                    if n_litters > rule.max_lifetime_litters:
                        warnings.append(_(
                            'Dam has %(n)s litters, exceeding the lifetime '
                            'limit of %(max)s.',
                            n=n_litters, max=rule.max_lifetime_litters,
                        ))
            rec.compliance_warning_count = len(warnings)
            if warnings:
                items = ''.join('<li>%s</li>' % w for w in warnings)
                rec.compliance_warning_html = '<ul class="mb-0">%s</ul>' % items
            else:
                rec.compliance_warning_html = False
