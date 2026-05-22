{
    'name': 'Petget: Australian Compliance',
    'version': '19.0.1.0.0',
    'category': 'Industries/Pet & Animal',
    'summary': 'Australian state breeding compliance rules and warnings',
    'description': """
Petget Australian Compliance
============================
Data-driven breeding compliance for the 8 Australian states/territories:
max fertile females per premise, lifetime litter limits, minimum sale age,
microchip age, and breeder ID requirements. Surfaces per-animal warnings.

Free and open source (AGPL-3) on the Odoo App Store. Production setup
(state config, data migration, deployment, training) is offered as a
professional service — see https://thepetget.com.
""",
    'author': 'BSD',
    'website': 'https://thepetget.com',
    'support': 'hello@thepetget.com',
    'license': 'AGPL-3',
    'images': ['static/description/banner.png'],
    'depends': [
        'petget_breeding_core',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/petget_compliance_au_rule_data.xml',
        'views/petget_compliance_au_rule_views.xml',
        'views/res_company_views.xml',
        'views/petget_animal_views.xml',
        'views/petget_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
