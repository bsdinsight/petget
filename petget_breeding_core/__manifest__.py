{
    'name': 'Petget: Breeding Core',
    'version': '19.0.1.0.0',
    'category': 'Industries/Pet & Animal',
    'summary': 'Breeding workflow for the Petget platform',
    'description': """
Petget Breeding Core
====================
Heat cycle, mating, pregnancy (species-aware gestation), and litter
management with one-by-one offspring creation. Builds on petget_core.
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
        'security/petget_breeding_security.xml',
        'security/ir.model.access.csv',
        'data/petget_breeding_sequence.xml',
        'views/petget_heat_cycle_views.xml',
        'views/petget_mating_views.xml',
        'views/petget_pregnancy_views.xml',
        'views/petget_litter_views.xml',
        'views/petget_animal_views.xml',
        'views/petget_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
