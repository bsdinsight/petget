{
    'name': 'Petnaly: Knowledge Base',
    'version': '19.0.1.0.0',
    'category': 'Industries/Pet & Animal',
    'summary': 'A breed library, care guides and stories for owners and breeders',
    'description': """
Petnaly Knowledge Base
=====================
A flexible content library that helps pet owners understand and care for
their dog — and helps breeders build the relationship that drives referrals.

Write rich articles and organise them by category (breed guide, care &
grooming, feeding & nutrition, training & behaviour, health & wellness,
stories & lore) and tags. Link an article to a specific breed so owners
see content relevant to the dog they actually have. Publish to make an
article visible to owners (e.g. in the companion mobile app).

Builds on the Petnaly dog breed catalogue.
""",
    'author': 'BSD',
    'website': 'https://petnaly.com',
    'support': 'hello@petnaly.com',
    'license': 'AGPL-3',
    'images': ['static/description/banner.png', 'static/description/screenshot1.png', 'static/description/screenshot2.png'],
    'depends': [
        'petnaly_dog',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/petnaly_kb_security.xml',
        'views/petnaly_kb_tag_views.xml',
        'views/petnaly_kb_article_views.xml',
        'views/petnaly_menus.xml',
        'data/petnaly_kb_data.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
