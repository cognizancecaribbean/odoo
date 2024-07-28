from odoo import models, fields

class ResPartnerBoat(models.Model):
    _name = 'members.management.boat'
    _description = 'Member Boat'

    name = fields.Char(string='Boat Name', required=True)
    size = fields.Char(string='Boat Size')
    engine = fields.Char(string='Boat Engine(s)')
    member_id = fields.Many2one('members.management.member', string='Member')
