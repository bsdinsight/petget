{
    'name': 'Petnaly: Breeding Core',
    'version': '19.0.1.0.0',
    'category': 'Industries/Pet & Animal',
    'summary': 'Breeding workflow for the Petnaly platform',
    'description': """
Petnaly Breeding Core
====================
Heat cycle, mating, pregnancy (species-aware gestation), and litter
management with one-by-one offspring creation. Builds on petnaly_core.
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
        'security/petnaly_breeding_security.xml',
        'security/ir.model.access.csv',
        'data/petnaly_breeding_sequence.xml',
        'views/petnaly_heat_cycle_views.xml',
        'views/petnaly_mating_views.xml',
        'views/petnaly_pregnancy_views.xml',
        'views/petnaly_litter_views.xml',
        'views/petnaly_animal_views.xml',
        'views/petnaly_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
