from odoo import models, fields

class ResPartnerDocument(models.Model):
    _name = 'res.partner.document'
    _description = 'Partner Document'

    name = fields.Char(string='Document Name', required=True)
    file = fields.Binary(string='File', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
