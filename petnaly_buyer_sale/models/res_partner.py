from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_buyer = fields.Boolean(string='Is a Buyer')
