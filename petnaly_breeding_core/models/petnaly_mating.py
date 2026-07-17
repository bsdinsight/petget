from datetime import timedelta

from odoo import _, api, fields, models

GESTATION_DAYS = {'dog': 63, 'cat': 65, 'horse': 340}


class PetnalyMating(models.Model):
    _name = 'petnaly.mating'
    _description = 'Mating Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'mating_date desc, id desc'

    name = fields.Char(compute='_compute_name', store=True)
    dam_id = fields.Many2one(
        'petnaly.animal', string='Dam', required=True, ondelete='cascade',
        index=True, domain=[('sex', '=', 'female')], tracking=True,
    )
    sire_id = fields.Many2one(
        'petnaly.animal', string='Sire', domain=[('sex', '=', 'male')],
        tracking=True,
    )
    external_sire = fields.Char(
        string='External Sire', help='Use when the sire is not in the database.',
    )
    external_sire_reg = fields.Char(string='External Sire Reg #')
    external_sire_owner = fields.Char(string='Stud Owner')

    # --- Method: natural vs artificial insemination ---
    mating_method = fields.Selection(
        selection=[('natural', 'Natural Mating'), ('ai', 'Artificial Insemination')],
        string='Method', default='natural', required=True, tracking=True,
    )
    ai_semen_type = fields.Selection(
        selection=[('fresh', 'Fresh'), ('chilled', 'Chilled'), ('frozen', 'Frozen')],
        string='Semen Type',
    )
    ai_technique = fields.Selection(
        selection=[
            ('vaginal', 'Vaginal'),
            ('tci', 'Transcervical (TCI)'),
            ('surgical', 'Surgical'),
        ],
        string='AI Technique',
    )
    attending_vet = fields.Char(string='Attending Vet')
    tie_observed = fields.Boolean(string='Tie / Lock Observed')
    supervised = fields.Boolean(string='Supervised')

    # --- Dates ---
    mating_date = fields.Date(string='Mating Date', required=True, tracking=True)
    mating_date_2 = fields.Date(string='Second Mating Date')
    heat_cycle_id = fields.Many2one(
        'petnaly.heat.cycle', string='Heat Cycle',
        domain="[('animal_id', '=', dam_id)]",
    )
    expected_due_date = fields.Date(
        string='Expected Due Date (est.)', compute='_compute_expected_due_date',
        help='Estimated from the mating date and the dam species gestation.',
    )

    # --- Outcome / commercial ---
    pregnancy_id = fields.Many2one(
        'petnaly.pregnancy', string='Pregnancy', readonly=True, copy=False,
    )
    stud_fee = fields.Monetary(string='Stud Fee')
    currency_id = fields.Many2one(
        'res.currency', related='company_id.currency_id',
    )
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one(
        'res.company', default=lambda self: self.env.company,
    )

    @api.depends('dam_id.name', 'sire_id.name', 'external_sire', 'mating_method')
    def _compute_name(self):
        for rec in self:
            sire = rec.sire_id.name or rec.external_sire or '?'
            suffix = ' (AI)' if rec.mating_method == 'ai' else ''
            rec.name = 'Mating: %s × %s%s' % (rec.dam_id.name or '?', sire, suffix)

    @api.depends('mating_date', 'dam_id.species')
    def _compute_expected_due_date(self):
        for rec in self:
            if rec.mating_date and rec.dam_id.species:
                days = GESTATION_DAYS.get(rec.dam_id.species, 63)
                rec.expected_due_date = rec.mating_date + timedelta(days=days)
            else:
                rec.expected_due_date = False

    def action_create_pregnancy(self):
        self.ensure_one()
        if self.pregnancy_id:
            preg = self.pregnancy_id
        else:
            preg = self.env['petnaly.pregnancy'].create({
                'dam_id': self.dam_id.id,
                'mating_id': self.id,
                'state': 'confirmed',
                'confirmation_date': fields.Date.context_today(self),
            })
            self.pregnancy_id = preg
        return {
            'type': 'ir.actions.act_window',
            'name': _('Pregnancy'),
            'res_model': 'petnaly.pregnancy',
            'res_id': preg.id,
            'view_mode': 'form',
            'target': 'current',
        }
