from odoo import models, fields

class ResPartnerOtherMembership(models.Model):
    _name = 'members.management.other_membership'
    _description = 'Member Other Membership'

    organization = fields.Char(string='Organization', required=True)
    role = fields.Char(string='Role')
    member_id = fields.Many2one('members.management.member', string='Member')
