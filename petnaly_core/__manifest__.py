{
    'name': 'Petnaly: Core',
    'version': '19.0.1.0.0',
    'category': 'Industries/Pet & Animal',
    'summary': 'Foundation models for the Petnaly breeding platform',
    'description': """
Petnaly Core
===========
Species-agnostic foundation for the Petnaly breeding management platform:
animal profile, documents, reminders, and audit timeline.

This is the skeleton module — models and views are added incrementally.
""",
    'author': 'BSD',
    'website': 'https://petnaly.com',
    'support': 'hello@petnaly.com',
    'license': 'AGPL-3',
    'images': ['static/description/banner.png', 'static/description/screenshot1.png', 'static/description/screenshot2.png'],
    'depends': [
        'base',
        'mail',
        'contacts',
    ],
    'data': [
        'security/petnaly_security.xml',
        'security/ir.model.access.csv',
        'data/petnaly_sequence.xml',
        'views/petnaly_animal_views.xml',
        'views/petnaly_document_views.xml',
        'views/petnaly_reminder_views.xml',
        'views/petnaly_note_views.xml',
        'views/petnaly_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
