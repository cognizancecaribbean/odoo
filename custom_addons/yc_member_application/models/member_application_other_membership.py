from odoo import models, fields

class MemberApplicationOtherMembership(models.Model):
    _name = 'member.application.other_membership'
    _description = 'Member Application Other Membership'

    organization = fields.Char(string='Organization', required=True)
    role = fields.Char(string='Role')
    application_id = fields.Many2one('member.application', string='Application')
