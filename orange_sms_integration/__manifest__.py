{
    'name': 'Orange SMS Integration',
    'version': '17.0.0',
    'category': 'Extra tools',
    'summary': 'Orange\'s SMS API Integration',
    'description': """
                SMS module for sending sms with Orange\'s SMS API
                """,
    'author': 'Social360',
    'website': 'www.social360mali.com',
    'license': 'AGPL-3',
    'depends': ['base', 'sms'],
    'data': [
        'security/ir.access.model.csv',
        'views/sms_config_settings_views.xml',
        'sms_template_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False
}