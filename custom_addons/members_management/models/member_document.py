from odoo import models, fields

class ResPartnerDocument(models.Model):
    _name = 'members.management.document'
    _description = 'Member Document'

    name = fields.Char(string='Document Name', required=True)
    file = fields.Binary(string='File', required=True)
    member_id = fields.Many2one('members.management.member', string='Member')
