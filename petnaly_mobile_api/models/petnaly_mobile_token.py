import secrets

from odoo import fields, models


class PetnalyMobileToken(models.Model):
    _name = 'petnaly.mobile.token'
    _description = 'Mobile API Token'
    _order = 'id desc'

    token = fields.Char(
        required=True, index=True, copy=False,
        default=lambda self: secrets.token_urlsafe(32),
    )
    user_id = fields.Many2one(
        'res.users', required=True, ondelete='cascade', index=True,
    )
    device_name = fields.Char()
    expires_at = fields.Datetime()
    last_used_at = fields.Datetime()
    active = fields.Boolean(default=True)
