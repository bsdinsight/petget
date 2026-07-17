from odoo import fields, models

from .petnaly_compliance_au_rule import AU_STATES


class ResCompany(models.Model):
    _inherit = 'res.company'

    petnaly_au_state = fields.Selection(
        selection=AU_STATES, string='Australian State/Territory',
        help='Used to apply the correct state breeding compliance rules.',
    )
