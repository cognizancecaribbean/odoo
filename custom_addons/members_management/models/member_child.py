from odoo import models, fields

class MemberChild(models.Model):
    _name = 'members.management.child'
    _description = 'Member Child'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    date_of_birth = fields.Date(string='Date of Birth', required=True)
    member_id = fields.Many2one('members.management.member', string='Member')
