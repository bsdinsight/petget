from odoo import fields, models


class PetnalyHeatProgesterone(models.Model):
    _name = 'petnaly.heat.progesterone'
    _description = 'Progesterone Reading'
    _order = 'test_date, id'

    heat_cycle_id = fields.Many2one(
        'petnaly.heat.cycle', string='Heat Cycle', required=True,
        ondelete='cascade', index=True,
    )
    test_date = fields.Date(string='Test Date', required=True)
    value_ngml = fields.Float(string='Progesterone (ng/mL)')
    note = fields.Char(string='Note')
