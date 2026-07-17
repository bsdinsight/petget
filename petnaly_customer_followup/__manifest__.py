{
    'name': 'Petnaly: Customer Follow-up',
    'version': '19.0.1.0.0',
    'category': 'Industries/Pet & Animal',
    'summary': 'Automatic customer care tasks after a sale',
    'description': """
Petnaly Customer Follow-up
=========================
Turns every sale into a relationship. When a puppy is marked sold, the
system generates a series of follow-up tasks (welcome call, check-ins,
vaccination reminders, anniversary) assigned to staff with due dates.
Staff phone/message the customer and mark each task done — building the
trust that drives repeat sales and referrals.

Steps are configurable templates. Tasks are NOT automated emails — they
are human touchpoints.
""",
    'author': 'BSD',
    'website': 'https://petnaly.com',
    'support': 'hello@petnaly.com',
    'license': 'AGPL-3',
    'images': ['static/description/banner.png'],
    'depends': [
        'petnaly_buyer_sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/petnaly_customer_followup_security.xml',
        'data/petnaly_followup_template_data.xml',
        'views/petnaly_followup_template_views.xml',
        'views/petnaly_followup_views.xml',
        'views/petnaly_reservation_views.xml',
        'views/res_partner_views.xml',
        'views/petnaly_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
