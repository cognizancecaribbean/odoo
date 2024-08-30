{
    'name': 'Members Management',
    'version': '1.0',
    'summary': 'Manage member applications, vetting, subscriptions, and billing',
    'description': """
        A comprehensive members module for managing member profiles, children, boats, documents, other memberships, and status tracking.
            • Handle everything from application to membership.
            • Custom fields and workflows for onboarding and membership status tracking.
            • Integration with the Subscription module for alerts on renewals.
            • Creation of tasks for staff to send new quotes. 
    """,
    'author': 'Cognizance Caribbean',
    'depends': ['base', 'contacts', 'mail', 'account'],
    'data': [
        # 'security/security.xml',
        'data/actions.xml',
        'security/ir.model.access.csv',
        'views/members_management_views.xml',
        'views/res_partner.xml',
        'report/report_member_application_template.xml',
        'report/report_action.xml',
    ],
    'installable': True,
    'application': True,
}
