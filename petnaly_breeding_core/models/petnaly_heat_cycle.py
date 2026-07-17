from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PetnalyHeatCycle(models.Model):
    _name = 'petnaly.heat.cycle'
    _description = 'Heat / Estrus Cycle'
    _inherit = ['mail.thread']
    _order = 'start_date desc, id desc'

    name = fields.Char(compute='_compute_name', store=True)
    animal_id = fields.Many2one(
        'petnaly.animal', string='Female', required=True, ondelete='cascade',
        index=True, domain=[('sex', '=', 'female')], tracking=True,
    )
    start_date = fields.Date(string='Start Date', required=True, tracking=True)
    end_date = fields.Date(string='End Date', tracking=True)
    state = fields.Selection(
        selection=[('ongoing', 'Ongoing'), ('completed', 'Completed')],
        string='Status', default='ongoing', required=True, tracking=True,
    )

    # --- Breeding timing ---
    standing_heat_start = fields.Date(
        string='Standing Heat (receptive) From',
        help='First day the female stands to be mated.',
    )
    ovulation_date = fields.Date(
        string='Estimated Ovulation',
        help='Usually estimated from progesterone testing.',
    )
    progesterone_ids = fields.One2many(
        'petnaly.heat.progesterone', 'heat_cycle_id', string='Progesterone Tests',
    )

    # --- Health / fitness ---
    fit_to_breed = fields.Selection(
        selection=[
            ('unknown', 'Not assessed'),
            ('fit', 'Fit to breed'),
            ('unfit', 'Not fit to breed'),
        ],
        string='Fitness to Breed', default='unknown',
    )
    vet_clearance = fields.Boolean(string='Pre-breeding Vet Clearance')
    vet_clearance_date = fields.Date(string='Vet Clearance Date')
    signs = fields.Text(
        string='Signs / Symptoms',
        help='Swelling, discharge colour, behaviour, flagging, etc.',
    )

    # --- Mating / regulatory tracking ---
    mating_ids = fields.One2many('petnaly.mating', 'heat_cycle_id', string='Matings')
    mating_count = fields.Integer(compute='_compute_mating')
    mated_this_cycle = fields.Boolean(
        string='Mated This Cycle', compute='_compute_mating', store=True,
    )
    cycle_length_days = fields.Integer(
        string='Cycle Length (days)', compute='_compute_cycle_length',
    )
    days_since_previous = fields.Integer(
        string='Days Since Previous Heat', compute='_compute_days_since_previous',
        help="Interval from this female's previous recorded heat — useful for "
             'cycle regularity and rest-between-seasons rules.',
    )

    notes = fields.Text(string='Notes')
    company_id = fields.Many2one(
        'res.company', default=lambda self: self.env.company,
    )

    @api.depends('animal_id.name', 'start_date')
    def _compute_name(self):
        for rec in self:
            label = rec.animal_id.name or '?'
            if rec.start_date:
                label = '%s (%s)' % (label, rec.start_date)
            rec.name = 'Heat: %s' % label

    @api.depends('mating_ids')
    def _compute_mating(self):
        for rec in self:
            rec.mating_count = len(rec.mating_ids)
            rec.mated_this_cycle = bool(rec.mating_ids)

    @api.depends('start_date', 'end_date')
    def _compute_cycle_length(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date >= rec.start_date:
                rec.cycle_length_days = (rec.end_date - rec.start_date).days
            else:
                rec.cycle_length_days = 0

    @api.depends('animal_id', 'start_date')
    def _compute_days_since_previous(self):
        for rec in self:
            rec.days_since_previous = 0
            if rec.animal_id and rec.start_date:
                prev = self.search([
                    ('animal_id', '=', rec.animal_id.id),
                    ('start_date', '<', rec.start_date),
                    ('id', '!=', rec.id),
                ], order='start_date desc', limit=1)
                if prev.start_date:
                    rec.days_since_previous = (rec.start_date - prev.start_date).days

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date < rec.start_date:
                raise ValidationError(
                    _('Heat cycle: the end date cannot be before the start date.'))

    def action_complete(self):
        self.write({'state': 'completed'})
