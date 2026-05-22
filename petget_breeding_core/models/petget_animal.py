from odoo import api, fields, models


class PetgetAnimal(models.Model):
    _inherit = 'petget.animal'

    litter_id = fields.Many2one('petget.litter', string='Birth Litter', index=True)
    birth_weight_g = fields.Float(string='Birth Weight (g)')
    birth_order = fields.Integer(string='Birth Order')
    heat_cycle_ids = fields.One2many(
        'petget.heat.cycle', 'animal_id', string='Heat Cycles',
    )
    pregnancy_ids = fields.One2many(
        'petget.pregnancy', 'dam_id', string='Pregnancies',
    )
    is_pregnant = fields.Boolean(
        string='Pregnant', compute='_compute_is_pregnant',
        search='_search_is_pregnant',
    )

    @api.depends('pregnancy_ids.state')
    def _compute_is_pregnant(self):
        for rec in self:
            rec.is_pregnant = any(
                state in ('suspected', 'confirmed')
                for state in rec.pregnancy_ids.mapped('state')
            )

    def _search_is_pregnant(self, operator, value):
        if operator not in ('=', '!='):
            raise NotImplementedError()
        active_preg = [('pregnancy_ids.state', 'in', ('suspected', 'confirmed'))]
        wants_pregnant = (operator == '=') == bool(value)
        return active_preg if wants_pregnant else ['!', *active_preg]
