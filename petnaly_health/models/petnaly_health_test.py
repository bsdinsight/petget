from odoo import api, fields, models


class PetnalyHealthTest(models.Model):
    _name = 'petnaly.health.test'
    _description = 'Animal Health Test'
    _order = 'test_date desc, id desc'

    name = fields.Char(compute='_compute_name', store=True)
    animal_id = fields.Many2one(
        'petnaly.animal', string='Animal', required=True, ondelete='cascade', index=True,
    )
    test_type = fields.Selection(
        selection=[
            ('hip_elbow', 'Hip & Elbow'),
            ('dna', 'DNA / Genetic'),
            ('eye', 'Eye (PRA, etc.)'),
            ('heart', 'Heart / Cardiac'),
            ('patella', 'Patella'),
            ('general', 'General / Other'),
        ],
        string='Test Type', required=True, default='hip_elbow',
    )
    test_date = fields.Date(string='Test Date')
    result = fields.Selection(
        selection=[
            ('clear', 'Clear / Pass'),
            ('carrier', 'Carrier'),
            ('affected', 'Affected / Fail'),
            ('pending', 'Pending'),
            ('na', 'N/A'),
        ],
        string='Result', default='clear',
    )
    result_detail = fields.Char(string='Result Detail')
    dna_marker = fields.Selection(
        selection=[
            ('prcd_pra', 'PRA (prcd-PRA)'),
            ('eic', 'Exercise-Induced Collapse (EIC)'),
            ('cnm', 'Centronuclear Myopathy (CNM)'),
            ('dm', 'Degenerative Myelopathy (DM)'),
            ('hnpk', 'Hereditary Nasal Parakeratosis (HNPK)'),
            ('sd2', 'Skeletal Dysplasia 2 (SD2)'),
            ('pkd', 'Pyruvate Kinase Deficiency (PK)'),
            ('rd_osd', 'RD / OSD'),
            ('other', 'Other'),
        ],
        string='DNA Marker',
    )
    provider = fields.Char(string='Provider / Radiologist')
    report_number = fields.Char(string='Report No.')

    # Hip & elbow specifics
    hip_score_total = fields.Integer(string='Hip Score (total)')
    hip_score_left = fields.Integer(string='Hip Left')
    hip_score_right = fields.Integer(string='Hip Right')
    elbow_grade_left = fields.Char(string='Elbow Left')
    elbow_grade_right = fields.Char(string='Elbow Right')
    breed_average = fields.Float(string='Breed Average')

    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    @api.depends('test_type', 'test_date', 'report_number')
    def _compute_name(self):
        labels = dict(self._fields['test_type'].selection)
        for rec in self:
            label = labels.get(rec.test_type, rec.test_type or 'Test')
            if rec.report_number:
                label = '%s #%s' % (label, rec.report_number)
            elif rec.test_date:
                label = '%s (%s)' % (label, rec.test_date)
            rec.name = label
