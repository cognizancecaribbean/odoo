{
    'name': 'CMP Administration',
    'version': '1.0',
    'category': 'Administration',
    'summary': 'Administrative tools for managing the election management system.',
    'description': """
        CMP Administration Module

        This module provides the administrative functionalities required to manage the election management system. It includes tools for:
        - Managing platform-wide data, including custom models for elections, voters, and addresses.
        - Overseeing user access and permissions across different branches and modules.
        - Managing data related to custom models such as Citizens, Voters, Streets, and Districts.
        - Integrating with other modules to ensure data consistency and manage election cycles.
        - Facilitating data imports and updates from external sources using Pandas for preprocessing.
        - Tracking changes and managing user access in the system.
        
        The CMP Administration module acts as the backbone for system management, enabling seamless integration and efficient management of election data and user roles.
    """,
    'author': 'Cognizance Caribbean Ltd.',
    'website': 'http://www.cognizancecaribbean.com',
    'depends': ['base', 'contacts'],
    'data': [
        # 'views/citizen_views.xml',
        # 'views/voter_views.xml',
        # 'views/address_views.xml',
        # 'views/street_views.xml',
        'views/polling_district_views.xml',
        'views/parliamentary_electoral_district_views.xml',
        'views/electoral_district_views.xml',
        'views/corporation_views.xml',
        'views/actions.xml',
        'views/election_mgnt_menus.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        # 'security/security.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
