{
    'name': 'Petnaly: Buyer & Sale',
    'version': '19.0.1.0.0',
    'category': 'Industries/Pet & Animal',
    'summary': 'Buyer, reservation, deposit and sale tracking',
    'description': """
Petnaly Buyer & Sale
===================
Practical baseline for the post-litter sales flow: buyers (on res.partner),
reservations with a deposit → sale state machine, and automatic ownership
transfer when a sale completes.

No invoicing or payment automation by design.

Free and open source (AGPL-3) on the Odoo App Store. Production setup is
offered as a professional service — see https://petnaly.com.
""",
    'author': 'BSD',
    'website': 'https://petnaly.com',
    'support': 'hello@petnaly.com',
    'license': 'AGPL-3',
    'images': ['static/description/banner.png', 'static/description/screenshot1.png'],
    'depends': [
        'petnaly_core',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/petnaly_buyer_sale_security.xml',
        'data/petnaly_buyer_sale_sequence.xml',
        'views/petnaly_reservation_views.xml',
        'views/res_partner_views.xml',
        'views/petnaly_animal_views.xml',
        'views/petnaly_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
