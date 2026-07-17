from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    followup_ids = fields.One2many(
        'petnaly.followup', 'buyer_id', string='Follow-ups',
    )
    followup_count = fields.Integer(
        string='Open Follow-ups', compute='_compute_followup_count',
    )

    @api.depends('followup_ids.state')
    def _compute_followup_count(self):
        for rec in self:
            rec.followup_count = len(
                rec.followup_ids.filtered(lambda f: f.state == 'pending')
            )

    def action_view_followups(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Follow-ups'),
            'res_model': 'petnaly.followup',
            'view_mode': 'list,form',
            'domain': [('buyer_id', '=', self.id)],
            'context': {'default_buyer_id': self.id},
        }
