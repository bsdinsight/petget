from odoo import _, api, fields, models


class PetnalyFollowup(models.Model):
    _name = 'petnaly.followup'
    _description = 'Customer Follow-up Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'due_date, id'

    name = fields.Char(string='Subject', required=True, tracking=True)
    buyer_id = fields.Many2one(
        'res.partner', string='Customer', required=True, tracking=True, index=True,
    )
    buyer_phone = fields.Char(related='buyer_id.phone', string='Phone', readonly=True)
    buyer_email = fields.Char(related='buyer_id.email', string='Email', readonly=True)
    animal_id = fields.Many2one('petnaly.animal', string='Animal')
    reservation_id = fields.Many2one(
        'petnaly.reservation', string='Reservation', index=True, ondelete='cascade',
    )
    user_id = fields.Many2one(
        'res.users', string='Assigned To', tracking=True,
        default=lambda self: self.env.user,
    )
    due_date = fields.Date(string='Due Date', tracking=True)
    state = fields.Selection(
        selection=[
            ('pending', 'To Do'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status', default='pending', required=True, tracking=True,
    )
    is_overdue = fields.Boolean(
        string='Overdue', compute='_compute_is_overdue', search='_search_is_overdue',
    )
    done_date = fields.Date(string='Completed On', readonly=True)
    note = fields.Text(string='Talking Points')
    company_id = fields.Many2one(
        'res.company', default=lambda self: self.env.company,
    )

    @api.depends('state', 'due_date')
    def _compute_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            rec.is_overdue = bool(
                rec.state == 'pending' and rec.due_date and rec.due_date < today
            )

    def _search_is_overdue(self, operator, value):
        if operator not in ('=', '!='):
            raise NotImplementedError()
        today = fields.Date.context_today(self)
        overdue = ['&', ('state', '=', 'pending'), ('due_date', '<', today)]
        not_overdue = ['|', ('state', '!=', 'pending'), ('due_date', '>=', today)]
        wants = (operator == '=') == bool(value)
        return overdue if wants else not_overdue

    def action_done(self):
        self.write({'state': 'done', 'done_date': fields.Date.context_today(self)})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_reset(self):
        self.write({'state': 'pending', 'done_date': False})
