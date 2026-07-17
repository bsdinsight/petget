from odoo import fields, models


class PetnalyDogColor(models.Model):
    _name = 'petnaly.dog.color'
    _description = 'Dog Colour'
    _order = 'name'

    name = fields.Char(string='Colour', required=True, translate=True)
    active = fields.Boolean(default=True)

    _name_uniq = models.Constraint('UNIQUE(name)', 'Colour must be unique.')
