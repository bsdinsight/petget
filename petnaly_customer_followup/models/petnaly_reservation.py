from datetime import timedelta

from odoo import _, fields, models


class PetnalyReservation(models.Model):
    _inherit = 'petnaly.reservation'

    followup_ids = fields.One2many(
        'petnaly.followup', 'reservation_id', string='Follow-ups',
    )
    followup_count = fields.Integer(
        string='Follow-up Count', compute='_compute_followup_count',
    )
    followup_generated = fields.Boolean(default=False, copy=False)

    def _compute_followup_count(self):
        for rec in self:
            rec.followup_count = len(rec.followup_ids)

    def _generate_followups(self):
        templates = self.env['petnaly.followup.template'].search([])
        Followup = self.env['petnaly.followup']
        for rec in self:
            if rec.followup_generated or not rec.buyer_id:
                continue
            base_date = rec.sale_date or fields.Date.context_today(rec)
            vals_list = [{
                'name': tpl.name,
                'buyer_id': rec.buyer_id.id,
                'animal_id': rec.animal_id.id,
                'reservation_id': rec.id,
                'user_id': self.env.user.id,
                'due_date': base_date + timedelta(days=tpl.offset_days),
                'note': tpl.note,
            } for tpl in templates]
            if vals_list:
                Followup.create(vals_list)
                rec.followup_generated = True

    def action_mark_sold(self):
        res = super().action_mark_sold()
        self._generate_followups()
        return res

    def action_generate_followups(self):
        self._generate_followups()

    def action_view_followups(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Follow-ups'),
            'res_model': 'petnaly.followup',
            'view_mode': 'list,form',
            'domain': [('reservation_id', '=', self.id)],
            'context': {
                'default_reservation_id': self.id,
                'default_buyer_id': self.buyer_id.id,
                'default_animal_id': self.animal_id.id,
            },
        }
