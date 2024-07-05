from odoo import models, fields, api

class MemberApplication(models.Model):
    _name = 'member.application'
    _description = 'Member Application'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    name = fields.Char(compute='_compute_name', store=True)
    other_names = fields.Char(string='Other Names')
    email = fields.Char(string='Email', required=True)
    profile_picture = fields.Binary(string='Profile Picture')

    date_of_birth = fields.Date(string='Date of Birth')
    street_address = fields.Char(string='Street Address')
    city = fields.Char(string='City / Town')
    country_id = fields.Many2one('res.country', string='Country')
    home_number = fields.Char(string='Home Number')
    office_number = fields.Char(string='Office Number')
    mobile_number = fields.Char(string='Mobile Number')
    marital_status = fields.Selection([('single', 'Single'), ('married', 'Married')], string='Marital Status')
    spouse_name = fields.Char(string='Spouse Name')

    children_ids = fields.One2many('member.application.child', 'application_id', string='Children')

    business_name = fields.Char(string='Business Name')
    business_street_address = fields.Char(string='Business Street Address')
    business_city = fields.Char(string='Business City / Town')
    business_country_id = fields.Many2one('res.country', string='Business Country')
    occupation = fields.Char(string='Occupation')
    nature_of_business = fields.Char(string='Nature of Business')

    document_ids = fields.One2many('member.application.document', 'application_id', string='Supporting Documents')
    member_type = fields.Selection([('regular', 'Regular'), ('premium', 'Premium')], string='Member Type')

    boat_ids = fields.One2many('member.application.boat', 'application_id', string='Boats')
    other_memberships_ids = fields.One2many('member.application.other_membership', 'application_id', string='Other Memberships')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('vetting', 'Vetting'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], default='draft', string='Status')

    def action_submit(self):
        self.state = 'submitted'
        # Send notification to staff

    def action_accept(self):
        self.state = 'accepted'
        partner = self.env['res.partner'].create({
            'is_member': True,
            'member_application_id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'other_names': self.other_names,
            'profile_picture': self.profile_picture,
            'date_of_birth': self.date_of_birth,
            'street_address': self.street_address,
            'city': self.city,
            'country_id': self.country_id.id,
            'home_number': self.home_number,
            'office_number': self.office_number,
            'mobile_number': self.mobile_number,
            'marital_status': self.marital_status,
            'spouse_name': self.spouse_name,
            'has_kids': self.has_kids,
            'children_ids': [(0, 0, {
                'first_name': child.first_name,
                'last_name': child.last_name,
                'date_of_birth': child.date_of_birth
            }) for child in self.children_ids],
            'business_name': self.business_name,
            'business_street_address': self.business_street_address,
            'business_city': self.business_city,
            'business_country_id': self.business_country_id.id,
            'occupation': self.occupation,
            'nature_of_business': self.nature_of_business,
            'document_ids': [(0, 0, {
                'name': doc.name,
                'file': doc.file
            }) for doc in self.document_ids],
            'membership_type': self.member_type,
            'member_since': fields.Date.today(),
            'boat_ids': [(0, 0, {
                'name': boat.name,
                'size': boat.size,
                'engine': boat.engine
            }) for boat in self.boat_ids],
            'other_memberships_ids': [(0, 0, {
                'organization': membership.organization,
                'role': membership.role
            }) for membership in self.other_memberships_ids],
        })
        self.env['sale.order'].create({
            'partner_id': partner.id,
            'order_line': [(0, 0, {
                'product_id': self.env.ref('product_membership').id,
                'product_uom_qty': 1,
                'price_unit': self.env.ref(f'membership.{self.member_type}_price').amount,
            })]
        }).action_confirm()

    def action_reject(self):
        self.state = 'rejected'



    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.first_name or ''} {record.last_name or ''}".strip()