from odoo import models, fields

class ResPartnerOtherMembership(models.Model):
    _name = 'res.partner.other_membership'
    _description = 'Partner Other Membership'

    organization = fields.Char(string='Organization', required=True)
    role = fields.Char(string='Role')
    partner_id = fields.Many2one('res.partner', string='Partner')
