from odoo import models, fields

class MemberApplicationDocument(models.Model):
    _name = 'member.application.document'
    _description = 'Member Application Document'

    name = fields.Char(string='Document Name', required=True)
    file = fields.Binary(string='File', required=True)
    application_id = fields.Many2one('member.application', string='Application')
