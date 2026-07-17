from odoo import _, api, fields, models


class PetnalyAnimal(models.Model):
    _inherit = 'petnaly.animal'

    health_test_ids = fields.One2many(
        'petnaly.health.test', 'animal_id', string='Health Tests',
    )
    health_test_count = fields.Integer(
        string='Health Test Count', compute='_compute_health',
    )
    has_hip_elbow = fields.Boolean(
        string='Hip/Elbow Tested', compute='_compute_health',
        search='_search_has_hip_elbow',
    )
    latest_hip_score = fields.Integer(
        string='Latest Hip Score', compute='_compute_health',
    )
    breeding_restricted = fields.Boolean(
        string='Not for Breeding (Limited Register)', tracking=True,
    )
    register_type = fields.Selection(
        selection=[('main', 'Main Register'), ('limited', 'Limited Register')],
        string='Register', default='main', tracking=True,
    )

    @api.depends('health_test_ids.test_type', 'health_test_ids.hip_score_total',
                 'health_test_ids.test_date')
    def _compute_health(self):
        for rec in self:
            rec.health_test_count = len(rec.health_test_ids)
            hips = rec.health_test_ids.filtered(
                lambda t: t.test_type == 'hip_elbow').sorted('test_date')
            rec.has_hip_elbow = bool(hips)
            rec.latest_hip_score = hips[-1].hip_score_total if hips else 0

    def _search_has_hip_elbow(self, operator, value):
        if operator not in ('=', '!='):
            raise NotImplementedError()
        has = [('health_test_ids.test_type', '=', 'hip_elbow')]
        wants = (operator == '=') == bool(value)
        return has if wants else ['!', *has]

    def action_view_health_tests(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Health Tests'),
            'res_model': 'petnaly.health.test',
            'view_mode': 'list,form',
            'domain': [('animal_id', '=', self.id)],
            'context': {'default_animal_id': self.id},
        }
