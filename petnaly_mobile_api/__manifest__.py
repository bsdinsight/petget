{
    'name': 'Petnaly: Mobile API',
    'version': '19.0.1.0.0',
    'category': 'Industries/Pet & Animal',
    'summary': 'REST/JSON API for the customer mobile app (B2C portal users)',
    'description': """
Petnaly Mobile API
=================
A token-authenticated REST/JSON API under /api/v1 for a customer-facing
mobile app. Customers self-register as Odoo portal users; data is isolated
per owner (a buyer sees only their own animals and the related documents,
health tests, pedigree and reminders).

Endpoints: health, auth/signup, auth/login, auth/forgot-password, me,
pets (list), pets/<id> (detail), documents/<id>/download.
""",
    'author': 'BSD',
    'website': 'https://petnaly.com',
    'support': 'hello@petnaly.com',
    'license': 'AGPL-3',
    'depends': [
        'petnaly_core',
        'portal',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/petnaly_mobile_security.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
