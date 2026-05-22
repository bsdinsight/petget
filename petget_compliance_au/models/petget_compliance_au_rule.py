from odoo import api, fields, models

AU_STATES = [
    ('nsw', 'New South Wales'),
    ('vic', 'Victoria'),
    ('qld', 'Queensland'),
    ('sa', 'South Australia'),
    ('wa', 'Western Australia'),
    ('tas', 'Tasmania'),
    ('nt', 'Northern Territory'),
    ('act', 'Australian Capital Territory'),
]


class PetgetComplianceAuRule(models.Model):
    _name = 'petget.compliance.au.rule'
    _description = 'Australian Compliance Rule by State'
    _order = 'state, species'

    name = fields.Char(compute='_compute_name', store=True)
    state = fields.Selection(selection=AU_STATES, string='State / Territory', required=True)
    species = fields.Selection(
        selection=[('dog', 'Dog'), ('cat', 'Cat')],
        string='Species', required=True, default='dog',
    )
    max_fertile_females = fields.Integer(
        string='Max Fertile Females',
        help='Maximum fertile females allowed per breeding premise. 0 = not configured.',
    )
    max_lifetime_litters = fields.Integer(string='Max Lifetime Litters', default=5)
    max_lifetime_litters_csection = fields.Integer(
        string='Max Lifetime Litters (with C-section)', default=3,
    )
    min_sale_age_weeks = fields.Integer(string='Min Sale Age (weeks)', default=8)
    microchip_required_age_weeks = fields.Integer(
        string='Microchip Required By (weeks)', default=12,
    )
    breeder_id_required = fields.Boolean(string='Breeder ID Required', default=True)
    citation = fields.Char(string='Legal Citation')
    active = fields.Boolean(default=True)

    _state_species_uniq = models.Constraint(
        'UNIQUE(state, species)',
        'There can be only one rule per state and species.',
    )

    @api.depends('state', 'species')
    def _compute_name(self):
        state_labels = dict(self._fields['state'].selection)
        species_labels = dict(self._fields['species'].selection)
        for rec in self:
            rec.name = '%s — %s' % (
                state_labels.get(rec.state, rec.state or '?'),
                species_labels.get(rec.species, rec.species or ''),
            )
