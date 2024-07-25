from odoo import models, fields

class ResPartnerChild(models.Model):
    _name = 'res.partner.child'
    _description = 'Partner Child'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    date_of_birth = fields.Date(string='Date of Birth', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
