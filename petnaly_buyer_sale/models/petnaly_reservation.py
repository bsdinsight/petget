from odoo import _, api, fields, models


class PetnalyReservation(models.Model):
    _name = 'petnaly.reservation'
    _description = 'Puppy Reservation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'reservation_date desc, id desc'

    name = fields.Char(
        string='Reservation', required=True, readonly=True, copy=False,
        default=lambda self: _('New'),
    )
    buyer_id = fields.Many2one(
        'res.partner', string='Buyer', required=True, tracking=True,
    )
    animal_id = fields.Many2one(
        'petnaly.animal', string='Animal', required=True, tracking=True,
        index=True,
    )
    reservation_date = fields.Date(
        string='Reservation Date', default=fields.Date.context_today,
        required=True,
    )
    state = fields.Selection(
        selection=[
            ('reserved', 'Reserved'),
            ('deposit', 'Deposit Received'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status', default='reserved', required=True, tracking=True,
    )
    deposit_amount = fields.Monetary(string='Deposit Amount')
    deposit_date = fields.Date(string='Deposit Date')
    sale_price = fields.Monetary(string='Sale Price')
    sale_date = fields.Date(string='Sale Date')
    note = fields.Text(string='Notes')
    currency_id = fields.Many2one(
        'res.currency', related='company_id.currency_id',
    )
    company_id = fields.Many2one(
        'res.company', default=lambda self: self.env.company,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == _('New'):
                vals['name'] = (
                    self.env['ir.sequence'].next_by_code('petnaly.reservation')
                    or _('New')
                )
        records = super().create(vals_list)
        for rec in records:
            if rec.buyer_id and not rec.buyer_id.is_buyer:
                rec.buyer_id.is_buyer = True
            if rec.animal_id and rec.state == 'reserved':
                rec.animal_id.sale_state = 'reserved'
        return records

    def action_mark_deposit(self):
        for rec in self:
            rec.state = 'deposit'
            if not rec.deposit_date:
                rec.deposit_date = fields.Date.context_today(rec)
            rec.animal_id.sale_state = 'deposit'

    def action_mark_sold(self):
        for rec in self:
            rec.state = 'sold'
            if not rec.sale_date:
                rec.sale_date = fields.Date.context_today(rec)
            rec.animal_id.write({
                'sale_state': 'sold',
                'owner_id': rec.buyer_id.id,
                'status': 'sold',
            })

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled'
            if rec.animal_id.sale_state in ('reserved', 'deposit'):
                rec.animal_id.sale_state = 'available'

    def action_reset_to_reserved(self):
        for rec in self:
            rec.state = 'reserved'
            rec.animal_id.sale_state = 'reserved'
