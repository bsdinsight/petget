{
    'name': 'Petnaly: Dog',
    'version': '19.0.1.0.0',
    'category': 'Industries/Pet & Animal',
    'summary': 'Dog species extension for the Petnaly platform',
    'description': """
Petnaly Dog
==========
Adds dog-specific data to the Petnaly animal profile: breed catalog
(AKC breeds pre-loaded), coat type, AKC registration, and puppy-stage
fields (temporary ID, collar colour). Dog fields appear only when the
animal's species is "Dog".
""",
    'author': 'BSD',
    'website': 'https://petnaly.com',
    'support': 'hello@petnaly.com',
    'license': 'AGPL-3',
    'images': ['static/description/banner.png', 'static/description/screenshot1.png', 'static/description/screenshot2.png'],
    'depends': [
        'petnaly_core',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/petnaly.dog.breed.csv',
        'views/petnaly_dog_breed_views.xml',
        'views/petnaly_animal_views.xml',
        'views/petnaly_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
