from odoo import fields, models


class PetgetFollowupTemplate(models.Model):
    _name = 'petget.followup.template'
    _description = 'Customer Follow-up Template'
    _order = 'sequence, offset_days'

    name = fields.Char(string='Subject', required=True, translate=True)
    sequence = fields.Integer(default=10)
    offset_days = fields.Integer(
        string='Days After Sale',
        help='The task falls due this many days after the sale date.',
    )
    note = fields.Text(string='Talking Points', translate=True)
    active = fields.Boolean(default=True)
