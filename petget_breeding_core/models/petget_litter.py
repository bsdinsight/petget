from odoo import _, api, fields, models


class PetgetLitter(models.Model):
    _name = 'petget.litter'
    _description = 'Litter Record'
    _inherit = ['mail.thread']
    _order = 'date_of_birth desc, id desc'

    name = fields.Char(
        string='Litter ID', required=True, readonly=True, copy=False,
        index=True, default=lambda self: _('New'),
    )
    # A litter originates from a confirmed pregnancy. Parents are taken from
    # that pregnancy and are read-only here.
    pregnancy_id = fields.Many2one('petget.pregnancy', string='Pregnancy', index=True)
    dam_id = fields.Many2one(
        'petget.animal', string='Dam', related='pregnancy_id.dam_id',
        store=True, readonly=True,
    )
    sire_id = fields.Many2one(
        'petget.animal', string='Sire', related='pregnancy_id.mating_id.sire_id',
        store=True, readonly=True,
    )
    external_sire = fields.Char(
        string='External Sire', related='pregnancy_id.mating_id.external_sire',
        store=True, readonly=True,
    )
    species = fields.Selection(related='dam_id.species', store=True)
    date_of_birth = fields.Date(string='Whelp Date', required=True)

    # --- Whelping ---
    whelping_method = fields.Selection(
        selection=[
            ('natural', 'Natural'),
            ('assisted', 'Assisted'),
            ('c_section', 'Caesarean (C-section)'),
        ],
        string='Whelping Method',
        help='C-sections count toward the lower lifetime-litter limit in some jurisdictions.',
    )
    vet_attended = fields.Boolean(string='Vet Attended')
    complications = fields.Text(string='Complications')

    # --- Counts ---
    total_offspring = fields.Integer(string='Number Born')
    born_alive = fields.Integer(string='Born Alive')
    stillborn = fields.Integer(string='Stillborn')
    deceased_neonatal = fields.Integer(string='Deceased (neonatal)')
    males_count = fields.Integer(string='Males')
    females_count = fields.Integer(string='Females')
    survived_count = fields.Integer(string='Surviving')
    average_birth_weight = fields.Float(
        string='Avg Birth Weight (g)', compute='_compute_avg_birth_weight',
    )

    # --- Registration ---
    litter_reg_number = fields.Char(string='Litter Registration #')
    litter_reg_date = fields.Date(string='Litter Registration Date')

    offspring_ids = fields.One2many(
        'petget.animal', 'litter_id', string='Puppies',
    )
    offspring_count = fields.Integer(
        string='Puppy Count', compute='_compute_offspring_count',
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('closed', 'Closed'),
        ],
        string='Status', default='draft', required=True, tracking=True,
    )
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one(
        'res.company', default=lambda self: self.env.company,
    )

    @api.depends('offspring_ids')
    def _compute_offspring_count(self):
        for rec in self:
            rec.offspring_count = len(rec.offspring_ids)

    @api.depends('offspring_ids.birth_weight_g')
    def _compute_avg_birth_weight(self):
        for rec in self:
            weights = [o.birth_weight_g for o in rec.offspring_ids if o.birth_weight_g]
            rec.average_birth_weight = round(sum(weights) / len(weights), 1) if weights else 0.0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == _('New'):
                vals['name'] = (
                    self.env['ir.sequence'].next_by_code('petget.litter')
                    or _('New')
                )
        return super().create(vals_list)

    def _puppy_default_context(self):
        self.ensure_one()
        return {
            'default_litter_id': self.id,
            'default_species': self.species or 'dog',
            'default_sire_id': self.sire_id.id,
            'default_dam_id': self.dam_id.id,
            'default_date_of_birth': self.date_of_birth,
            'default_status': 'young',
        }

    def action_add_puppy(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('New Puppy'),
            'res_model': 'petget.animal',
            'view_mode': 'form',
            'target': 'current',
            'context': self._puppy_default_context(),
        }

    def action_view_offspring(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Puppies'),
            'res_model': 'petget.animal',
            'view_mode': 'list,form',
            'domain': [('litter_id', '=', self.id)],
            'context': self._puppy_default_context(),
        }
