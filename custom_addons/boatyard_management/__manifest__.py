{
    'name': 'Boatyard Management',
    'version': '1.0',
    'summary': 'Manage events, spaces, space booking with invoicing',
    'description': """
        A comprehensive boatyard management module to manage data for boats, boat spaces, boat movements and invoicing customers.
            • Maintain boat specification record
            • Maintain boat engine data
            • Maintain record of boat devices
            • Maintain record of boat documents
            • Maintain a list of all spaces allocated for parking boats with interactive property map
                1. Manage the occupation and booking of boat spaces by members and non-members
                2. Schedule and maintain records of boat movements
    """,
    'author': 'Cognizance Caribbean',
    'depends': ['base', 'mail', 'sale_management', 'web'],
    'data': [
        'data/actions.xml',
        'security/ir.model.access.csv',
        'views/boatyard_views.xml',
        'views/boat_specification_views.xml',
        'views/menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'boatyard_management/static/src/boatyard_map/boatyard_map.js',
            'boatyard_management/static/src/boatyard_map/boatyard_map_template.xml',
            'boatyard_management/static/src/css/boatyard_map.css',
        ],
    },     
    'installable': True,
    'application': True,
}