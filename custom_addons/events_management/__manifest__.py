{
    'name': 'Events Management',
    'version': '1.0',
    'summary': 'Manage events, spaces, space booking with invoicing',
    'description': """
        A comprehensive events management module to manage data for evens, event spaces, space bookings and invoicing customers.
            • Event creation and approval
            • Automated notifications and reminders
            • Booking request and approval process 
            • Invoicing for booked spaces via  Odoo’s Invoicing app.
            • Space availability checking and booking management 
            • Automated notifications for booking confirmations and reminders
            • Create and print rental agreement / application form 
    """,
    'author': 'Cognizance Caribbean',
    'depends': ['base', 'mail', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/space_amenity_views.xml',
        'views/event_views.xml',
        'views/event_space_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
}