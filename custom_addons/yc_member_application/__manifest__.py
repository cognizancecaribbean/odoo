{
    'name': 'Yatch Club Member Application',
    'version': '1.0',
    'summary': 'Manage member applications, vetting, and onboarding',
    'description': """
        Module to handle member applications, vetting, and onboarding.
    """,
    'author': 'Cognizance Caribbean',
    'depends': ['base', 'website', 'sale'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/member_application_views.xml',
        'views/res_partner_views.xml',
        'views/templates.xml',
        'data/data.xml',
    ],
    'installable': True,
    'application': True,
}
