from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

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
        ('welcome', 'Welcome Letter Sent'),
        ('orientation', 'Orientation Notice'),
        ('bylaws', 'Bylaws Sent'),
    ], string='Application State', default='new')
    
    # Application process tracking
    application_date = fields.Date(string='Application Date')
    acknowledgment_date = fields.Date(string='Acknowledgment Date')
    interview_notice_date = fields.Date(string='Notice of Interview Date')
    interview_date = fields.Date(string='Interview Date')
    followup_date = fields.Date(string='Followup Date')
    welcome_letter_date = fields.Date(string='Welcome Letter Date')
    orientation_notice_date = fields.Date(string='Orientation Notice Date')
    orientation_date = fields.Date(string='Orientation Date')
    bylaws_sent_date = fields.Date(string='Bylaws Sent Date')

    # Profile Data
    # Add method calculate value for existing name field
    first_name = fields.Char(string='First Name')
    last_name = fields.Char(string='Last Name')
    other_names = fields.Char(string='Other Names')
    # profile_picture = fields.Binary(string='Profile Picture') # Use existing image field
    date_of_birth = fields.Date(string='Date of Birth')
    # street_address = fields.Char(string='Street Address') # Use existing street and street2 fields
    # city = fields.Char(string='City / Town') # Use existing city field
    # country_id = fields.Many2one('res.country', string='Country') # Use existing country_id field
    # home_number = fields.Char(string='Home Number') # Use existing phone field
    office_number = fields.Char(string='Office Number')
    # mobile_number = fields.Char(string='Mobile Number') # Use existing mobile field
    marital_status = fields.Selection([('single', 'Single'), ('married', 'Married')], string='Marital Status')
    spouse_name = fields.Char(string='Spouse Name')

    # Children Data
    has_kids = fields.Boolean(string='Has Kids')
    children_ids = fields.One2many('res.partner.child', 'partner_id', string='Children')

    # Business Data
    business_name = fields.Char(string='Business Name')
    business_street_address = fields.Char(string='Business Street Address')
    business_city = fields.Char(string='Business City / Town')
    business_country_id = fields.Many2one('res.country', string='Business Country')
    occupation = fields.Char(string='Occupation')
    nature_of_business = fields.Char(string='Nature of Business')

    # Supporting Documents
    document_ids = fields.One2many('res.partner.document', 'partner_id', string='Supporting Documents')

    # Membership Data
    membership_type = fields.Selection([('regular', 'Regular'), ('premium', 'Premium')], string='Member Type')
    member_since = fields.Date(string='Member Since')

    # Boat Data
    boat_ids = fields.One2many('res.partner.boat', 'partner_id', string='Boats')

    # Other Memberships
    other_memberships_ids = fields.One2many('res.partner.other_membership', 'partner_id', string='Other Memberships')


    # Automated status transition method
    @api.model
    def update_status(self, new_status):
        self.status = new_status

    # Automated state transition method
    @api.model
    def update_application_state(self, new_state):
        self.application_state = new_state

    # Method to calculate full name if needed
    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for record in self:
            record.name = f"{record.first_name} {record.last_name}" if record.first_name and record.last_name else ''

    # Constraints
    _sql_constraints = [
        ('unique_email', 'unique(email)', 'A partner with this email already exists!')
    ]