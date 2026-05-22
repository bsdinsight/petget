{
    'name': 'Petget: Buyer & Sale',
    'version': '19.0.1.0.0',
    'category': 'Industries/Pet & Animal',
    'summary': 'Buyer, reservation, deposit and sale tracking',
    'description': """
Petget Buyer & Sale
===================
Practical baseline for the post-litter sales flow: buyers (on res.partner),
reservations with a deposit → sale state machine, and automatic ownership
transfer when a sale completes.

No invoicing or payment automation by design.

Free and open source (AGPL-3) on the Odoo App Store. Production setup is
offered as a professional service — see https://thepetget.com.
""",
    'author': 'BSD',
    'website': 'https://thepetget.com',
    'support': 'hello@thepetget.com',
    'license': 'AGPL-3',
    'images': ['static/description/banner.png'],
    'depends': [
        'petget_core',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/petget_buyer_sale_security.xml',
        'data/petget_buyer_sale_sequence.xml',
        'views/petget_reservation_views.xml',
        'views/res_partner_views.xml',
        'views/petget_animal_views.xml',
        'views/petget_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
