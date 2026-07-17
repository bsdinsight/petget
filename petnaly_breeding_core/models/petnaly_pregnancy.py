from datetime import timedelta

from odoo import _, api, fields, models


class PetnalyPregnancy(models.Model):
    _name = 'petnaly.pregnancy'
    _description = 'Pregnancy Record'
    _inherit = ['mail.thread']
    _order = 'id desc'

    GESTATION_DAYS = {'dog': 63, 'cat': 65, 'horse': 340}

    name = fields.Char(compute='_compute_name', store=True)
    dam_id = fields.Many2one(
        'petnaly.animal', string='Dam', required=True, ondelete='cascade',
        index=True, domain=[('sex', '=', 'female')], tracking=True,
    )
    mating_id = fields.Many2one('petnaly.mating', string='Mating')
    species = fields.Selection(related='dam_id.species', store=True)
    confirmation_date = fields.Date(string='Confirmation Date', tracking=True)
    confirmation_method = fields.Selection(
        selection=[
            ('ultrasound', 'Ultrasound'),
            ('xray', 'X-ray'),
            ('palpation', 'Palpation'),
            ('relaxin', 'Blood test (relaxin)'),
            ('other', 'Other'),
        ],
        string='Confirmation Method',
    )
    confirmed_by = fields.Char(string='Confirmed By (Vet)')
    puppy_count_estimate = fields.Integer(
        string='Estimated Offspring',
        help='Expected number of offspring, e.g. from an X-ray count.',
    )
    expected_due_date = fields.Date(
        string='Expected Due Date', compute='_compute_expected_due_date',
        store=True,
    )
    actual_birth_date = fields.Date(string='Actual Birth Date')
    state = fields.Selection(
        selection=[
            ('suspected', 'Suspected'),
            ('confirmed', 'Confirmed'),
            ('delivered', 'Delivered'),
            ('failed', 'Failed / Resorbed'),
        ],
        string='Status', default='suspected', required=True, tracking=True,
    )
    litter_id = fields.Many2one(
        'petnaly.litter', string='Litter', readonly=True, copy=False,
    )
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one(
        'res.company', default=lambda self: self.env.company,
    )

    @api.depends('dam_id.name')
    def _compute_name(self):
        for rec in self:
            rec.name = 'Pregnancy: %s' % (rec.dam_id.name or '?')

    @api.depends('mating_id.mating_date', 'dam_id.species')
    def _compute_expected_due_date(self):
        for rec in self:
            mating_date = rec.mating_id.mating_date
            species = rec.dam_id.species
            if mating_date and species:
                days = rec.GESTATION_DAYS.get(species, 63)
                rec.expected_due_date = mating_date + timedelta(days=days)
            else:
                rec.expected_due_date = False

    def action_confirm(self):
        self.write({
            'state': 'confirmed',
            'confirmation_date': fields.Date.context_today(self),
        })

    def action_fail(self):
        self.write({'state': 'failed'})

    def action_create_litter(self):
        self.ensure_one()
        if self.litter_id:
            litter = self.litter_id
        else:
            litter = self.env['petnaly.litter'].create({
                'pregnancy_id': self.id,
                'date_of_birth': self.actual_birth_date or fields.Date.context_today(self),
            })
            self.litter_id = litter
        self.write({
            'state': 'delivered',
            'actual_birth_date': self.actual_birth_date or fields.Date.context_today(self),
        })
        return {
            'type': 'ir.actions.act_window',
            'name': _('Litter'),
            'res_model': 'petnaly.litter',
            'res_id': litter.id,
            'view_mode': 'form',
            'target': 'current',
        }
