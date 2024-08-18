{
    'name': 'Mobile Money Payment',
    'version': '17.0.0',
    'category': 'Payment',
    'summary': 'Mobile Money Payment',
    'description': """
                This module is use for Mobile Money Payment for a lot of Africa's countries
                """,
    'authors': 'logic_dev',
    'license': 'AGPL-3',
    'depends': ['base', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/donation_template.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}