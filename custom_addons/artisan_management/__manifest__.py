{
    'name': "Artisan Management",
    'summary': "Module to manage profiles of trained artisans and dashboard",
    'description': """
        Module to facilitate the onboarding and management of local artisan data
    """,
    'author': "Cognizance Caribbean Ltd.",
    'website': "https://cognizancecaribbean.com",
    'version': '0.1',
    'depends': ['base', 'mail', 'web', 'website', 'web_editor'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'reports/report_artisans_by_state.xml',
        'reports/report_artisans_by_activity_type.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'artisan_management/static/src/artisan_dashboard/totals_card.js',
            'artisan_management/static/src/artisan_dashboard/totals_card_template.xml',
            'artisan_management/static/src/artisan_dashboard/tags_table.js',
            'artisan_management/static/src/artisan_dashboard/tags_table_template.xml',
            'artisan_management/static/src/artisan_dashboard/artisan_dashboard.js',
            'artisan_management/static/src/artisan_dashboard/artisan_dashboard_template.xml',
            'https://cdn.jsdelivr.net/npm/chart.js',
        ],
        'web.assets_frontend': [
            'web/static/lib/jquery/jquery.js',
            'artisan_management/static/src/js/registration_form.js',
        ]
    },
    'installable': True,
    'application': True,
}
