from odoo import models, fields, api
from datetime import timedelta


class Member(models.Model):
    _name = 'members.management.member'
    _description = 'Members'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    status = fields.Selection([
        ('applicant', 'Applicant'),
        ('member', 'Member'),
        ('rejected', 'Rejected')
    ], string='Status', default='applicant')
    
    application_state = fields.Selection([
        ('new', 'New Applicant'),
        ('acknowledged', 'Receipt Acknowledged'),
        ('interview', 'Notice of Interview'),
        ('followup', 'Followup Letter Sent'),
        ('welcomed', 'Welcome Letter Sent'),
        ('orientation', 'Orientation Notice'),
        ('bylaws', 'Bylaws Sent'),
        ('quote_sent', 'Quote Sent'),
        ('quote_signed', 'Quote Signed'),
        ('sub_initialized', 'Subscription Initialized'),
    ], string='Application State', default='new')
    
    # Application process tracking
    application_date = fields.Date(string='Application Date')
    acknowledgment_date = fields.Date(string='Acknowledgment Date')
    interview_notice_date = fields.Date(string='Notice of Interview Date')
    interview_date = fields.Date(string='Interview Date')
    followup_date = fields.Date(string='Followup Letter Date')
    welcome_letter_date = fields.Date(string='Welcome Letter Date')
    orientation_notice_date = fields.Date(string='Orientation Notice Date')
    orientation_date = fields.Date(string='Orientation Date')
    bylaws_sent_date = fields.Date(string='Bylaws Sent Date')
    quote_sent_date = fields.Date(string='Quote Sent Date')
    quote_signed_date = fields.Date(string='Quote Signed Date')
    sub_initialized_date = fields.Date(string='Subscription Initialization Date')
    
    # Subscription state
    subscription_state = fields.Selection([
        ('active', 'Active'),
        ('expiring', 'Expiring'),
        ('expired', 'Expired'),
        ('inactive', 'Inactive'),
        ('d_suspended', 'Disciplinary Suspension'),
        ('v_suspended', 'Voluntary Suspension'),
    ], string='Subscription State', default='inactive', tracking=True)    

    # Profile Data
    # Add method calculate value for existing name field
    first_name = fields.Char(string='First Name')
    last_name = fields.Char(string='Last Name')
    other_names = fields.Char(string='Other Names')
    email = fields.Char(string="Email Address", required=True, tracking=True)
    profile_picture = fields.Binary(string='Profile Picture') # Use to manage partner's image field
    date_of_birth = fields.Date(string='Date of Birth')
    # Use existing street and street2 fields
    street_address = fields.Char(string='Street Address') 
    street_address2 = fields.Char(string='Street Address 2') 
    city = fields.Char(string='City') # Use to manage partner's city field
    zip = fields.Char(string='Zip')
    state_id = fields.Many2one('res.state', string='State') # Use to manage partner's state_id field
    country_id = fields.Many2one('res.country', string='Country') # Use to manage partner's country_id field
    home_number = fields.Char(string='Home Number') # Use to manage partner's phone field
    office_number = fields.Char(string='Office Number')
    mobile_number = fields.Char(string='Mobile Number') # Use to manage partner's mobile field
    marital_status = fields.Selection([('single', 'Single'), ('married', 'Married')], string='Marital Status')
    spouse_name = fields.Char(string='Spouse Name')

    # Children Data
    has_kids = fields.Boolean(string='Has Kids')
    children_ids = fields.One2many('members.management.child', 'member_id', string='Children')

    # Business Data
    business_name = fields.Char(string='Business Name')
    business_street_address = fields.Char(string='Business Street Address')
    business_city = fields.Char(string='Business City / Town')
    business_country_id = fields.Many2one('res.country', string='Business Country')
    occupation = fields.Char(string='Occupation')
    nature_of_business = fields.Text(string='Nature of Business')

    # Supporting Documents
    document_ids = fields.One2many('members.management.document', 'member_id', string='Supporting Documents')

    # Membership Data
    membership_type = fields.Selection([('regular', 'Regular'), ('premium', 'Premium')], string='Member Type')
    member_since = fields.Date(string='Member Since')

    # Boat Data
    boat_ids = fields.One2many('members.management.boat', 'member_id', string='Boats')

    # Other Memberships
    other_memberships_ids = fields.One2many('members.management.other_membership', 'member_id', string='Other Memberships')
    
    partner_id = fields.Many2one('res.partner', string='Related Partner')
    
    # Computed name field
    name = fields.Char(string='Name', compute='_compute_name', store=True)
    

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.first_name} {record.last_name}"
            
    @api.model
    def create(self, vals):
        # Set the application date when a new record is created
        vals['application_date'] = fields.Date.today()
        # Call the super method to create the member
        return super(Member, self).create(vals)            
        
    @api.model
    def create_partner(self):
        # Create a partner record with default fields
        partner_vals = {
            'name': f"{self.first_name} {self.last_name}",
            'image_1920': self.profile_picture,
            'street': self.street_address,
            'street2': self.street_address2,
            'city': self.city,
            'zip': self.zip,
            'state_id': self.state_id.id,
            'country_id': self.country_id.id,
            'phone': self.home_number,
            'mobile': self.mobile_number,
            'email': self.email,  # Ensure email field is present if used
            'is_company': False,  # Ensure the partner is set as a person
            'is_member': True,  # Custom field to mark as member
        }
        partner = self.env['res.partner'].create(partner_vals)
        self.partner_id = partner.id

    @api.model
    def accept_application(self):
        for record in self:
            if record.status != 'accepted':
                record.status = 'accepted'
                record.create_partner()
                
    @api.model
    def update_subscription_state(self):
        # Fetch the subscription data and update the subscription_state field
        subscription_obj = self.env['sale.subscription']
        members = self.search([('status', '=', 'member')])

        for member in members:
            subscriptions = subscription_obj.search([('partner_id', '=', member.partner_id.id)])
            if subscriptions:
                for subscription in subscriptions:
                    if subscription.recurring_next_date:
                        # Calculate the state based on the next recurring date
                        if subscription.recurring_next_date <= fields.Date.today():
                            member.subscription_state = 'expired'
                        elif subscription.recurring_next_date <= (fields.Date.today() + timedelta(days=30)):
                            member.subscription_state = 'expiring'
                        else:
                            member.subscription_state = 'active'
                    else:
                        member.subscription_state = 'inactive'
            else:
                member.subscription_state = 'inactive'

    # Schedule this method to run periodically to keep the subscription state updated                

    # Constraints
    _sql_constraints = [
        ('unique_email', 'unique(email)', 'A member or applicant with this email already exists!')
    ]