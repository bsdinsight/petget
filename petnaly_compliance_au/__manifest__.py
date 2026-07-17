{
    'name': 'Petnaly: Australian Compliance',
    'version': '19.0.1.0.0',
    'category': 'Industries/Pet & Animal',
    'summary': 'Australian state breeding compliance rules and warnings',
    'description': """
Petnaly Australian Compliance
============================
Data-driven breeding compliance for the 8 Australian states/territories:
max fertile females per premise, lifetime litter limits, minimum sale age,
microchip age, and breeder ID requirements. Surfaces per-animal warnings.

Free and open source (AGPL-3) on the Odoo App Store. Production setup
(state config, data migration, deployment, training) is offered as a
professional service — see https://petnaly.com.
""",
    'author': 'BSD',
    'website': 'https://petnaly.com',
    'support': 'hello@petnaly.com',
    'license': 'AGPL-3',
    'images': ['static/description/banner.png'],
    'depends': [
        'petnaly_breeding_core',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/petnaly_compliance_au_rule_data.xml',
        'views/petnaly_compliance_au_rule_views.xml',
        'views/res_company_views.xml',
        'views/petnaly_animal_views.xml',
        'views/petnaly_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
