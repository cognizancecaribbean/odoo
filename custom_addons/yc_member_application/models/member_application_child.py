from odoo import models, fields

class MemberApplicationChild(models.Model):
    _name = 'member.application.child'
    _description = 'Member Application Child'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    date_of_birth = fields.Date(string='Date of Birth', required=True)
    application_id = fields.Many2one('member.application', string='Application')
