from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_member = fields.Boolean(string='Is a Member', default=False)
    member_application_id = fields.Many2one('member.application', string='Member Application')

    # Account Data
    first_name = fields.Char(string='First Name')
    last_name = fields.Char(string='Last Name')
    other_names = fields.Char(string='Other Names')
    profile_picture = fields.Binary(string='Profile Picture')

    # Profile Data
    date_of_birth = fields.Date(string='Date of Birth')
    street_address = fields.Char(string='Street Address')
    city = fields.Char(string='City / Town')
    country_id = fields.Many2one('res.country', string='Country')
    home_number = fields.Char(string='Home Number')
    office_number = fields.Char(string='Office Number')
    mobile_number = fields.Char(string='Mobile Number')
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
