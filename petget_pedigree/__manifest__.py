{
    'name': 'Petget: Pedigree & Registration',
    'version': '19.0.1.0.0',
    'category': 'Industries/Pet & Animal',
    'summary': 'Registration details and a multi-generation pedigree tree',
    'description': """
Petget Pedigree & Registration
==============================
Adds registration details (registry body, country of origin) and a
multi-generation pedigree view to each animal. The pedigree tree is built
from the sire/dam links, showing up to three generations of ancestors.
Ancestor records can be flagged as pedigree-only so they stay out of the
day-to-day animal list.
""",
    'author': 'BSD',
    'website': 'https://thepetget.com',
    'support': 'hello@thepetget.com',
    'license': 'AGPL-3',
    'images': ['static/description/banner.png', 'static/description/screenshot1.png'],
    'depends': [
        'petget_core',
    ],
    'data': [
        'views/petget_animal_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
