{
    'name': 'Petnaly: Health Screening',
    'version': '19.0.1.0.0',
    'category': 'Industries/Pet & Animal',
    'summary': 'Hip/elbow, DNA and other health tests, with breeding clearance warnings',
    'description': """
Petnaly Health Screening
=======================
Capture structured health-test results — hip & elbow scores (with breed
average), DNA/genetic, eye, heart and more — on each animal. Flag dogs as
Not for Breeding (Limited Register). When recording a mating, the system
warns if a parent is breeding-restricted or has no hip/elbow clearance on
record, helping breeders make sound, defensible decisions.
""",
    'author': 'BSD',
    'website': 'https://petnaly.com',
    'support': 'hello@petnaly.com',
    'license': 'AGPL-3',
    'images': ['static/description/banner.png', 'static/description/screenshot1.png'],
    'depends': [
        'petnaly_breeding_core',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/petnaly_health_security.xml',
        'views/petnaly_health_test_views.xml',
        'views/petnaly_animal_views.xml',
        'views/petnaly_mating_views.xml',
        'views/petnaly_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
