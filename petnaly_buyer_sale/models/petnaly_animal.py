from odoo import _, api, fields, models


class PetnalyAnimal(models.Model):
    _inherit = 'petnaly.animal'

    sale_state = fields.Selection(
        selection=[
            ('available', 'Available'),
            ('reserved', 'Reserved'),
            ('deposit', 'Deposit Received'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
            ('retained', 'Retained'),
        ],
        string='Sale Status', default='available', tracking=True,
    )
    reservation_ids = fields.One2many(
        'petnaly.reservation', 'animal_id', string='Reservations',
    )
    reservation_count = fields.Integer(
        string='Reservation Count', compute='_compute_reservation_count',
    )

    @api.depends('reservation_ids')
    def _compute_reservation_count(self):
        for rec in self:
            rec.reservation_count = len(rec.reservation_ids)

    def action_view_reservations(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Reservations'),
            'res_model': 'petnaly.reservation',
            'view_mode': 'list,form',
            'domain': [('animal_id', '=', self.id)],
            'context': {'default_animal_id': self.id},
        }
