from odoo import fields, models


class PetnalyKbTag(models.Model):
    _name = 'petnaly.kb.tag'
    _description = 'Knowledge Base Tag'
    _order = 'name'

    name = fields.Char(string='Tag', required=True, index='trigram')
    color = fields.Integer(string='Color')

    _name_uniq = models.Constraint('UNIQUE(name)', 'Tag name must be unique.')
