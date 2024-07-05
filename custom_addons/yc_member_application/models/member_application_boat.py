from odoo import models, fields

class MemberApplicationBoat(models.Model):
    _name = 'member.application.boat'
    _description = 'Member Application Boat'

    name = fields.Char(string='Boat Name', required=True)
    size = fields.Char(string='Boat Size')
    engine = fields.Char(string='Boat Engine')
    application_id = fields.Many2one('member.application', string='Application')
