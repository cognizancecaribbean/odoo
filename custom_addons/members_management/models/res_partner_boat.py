from odoo import models, fields

class ResPartnerBoat(models.Model):
    _name = 'res.partner.boat'
    _description = 'Partner Boat'

    name = fields.Char(string='Boat Name', required=True)
    size = fields.Char(string='Boat Size')
    engine = fields.Char(string='Boat Engine')
    partner_id = fields.Many2one('res.partner', string='Partner')
