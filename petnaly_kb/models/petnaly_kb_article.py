import re

from odoo import api, fields, models


class PetnalyKbArticle(models.Model):
    _name = 'petnaly.kb.article'
    _description = 'Knowledge Base Article'
    _inherit = ['mail.thread', 'image.mixin']
    _order = 'sequence, date_published desc, id desc'

    name = fields.Char(string='Title', required=True, tracking=True, index='trigram')
    subtitle = fields.Char(string='Subtitle')
    category = fields.Selection(
        selection=[
            ('breed', 'Breed Guide'),
            ('care', 'Care & Grooming'),
            ('nutrition', 'Feeding & Nutrition'),
            ('training', 'Training & Behaviour'),
            ('health', 'Health & Wellness'),
            ('story', 'Stories & Lore'),
            ('general', 'General'),
        ],
        string='Category', required=True, default='general', tracking=True,
    )
    species = fields.Selection(
        selection=[('dog', 'Dog'), ('cat', 'Cat'), ('horse', 'Horse'), ('other', 'Other')],
        string='Species', default='dog',
    )
    breed_id = fields.Many2one(
        'petnaly.dog.breed', string='Breed',
        help='Link to a breed when the article is breed-specific.',
    )
    summary = fields.Text(
        string='Summary',
        help='Short teaser shown in lists and the mobile app.',
    )
    body = fields.Html(string='Content', sanitize=True)
    tag_ids = fields.Many2many('petnaly.kb.tag', string='Tags')
    author_id = fields.Many2one(
        'res.users', string='Author', default=lambda self: self.env.user,
    )
    published = fields.Boolean(
        string='Published', default=False, tracking=True,
        help='Only published articles are shown to pet owners in the app.',
    )
    date_published = fields.Date(string='Publish Date')
    reading_minutes = fields.Integer(
        string='Read (min)', compute='_compute_reading_minutes', store=True,
    )
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        'res.company', default=lambda self: self.env.company,
    )

    @api.depends('body')
    def _compute_reading_minutes(self):
        for rec in self:
            text = re.sub(r'<[^>]+>', ' ', rec.body or '')
            words = len(text.split())
            rec.reading_minutes = max(1, round(words / 200.0)) if words else 0

    def action_publish(self):
        for rec in self:
            rec.published = True
            if not rec.date_published:
                rec.date_published = fields.Date.context_today(rec)

    def action_unpublish(self):
        self.write({'published': False})
