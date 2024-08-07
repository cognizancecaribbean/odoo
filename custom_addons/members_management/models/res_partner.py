from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_member = fields.Boolean(string='Is a Member')
    boat_ids = fields.Many2many('members.management.boat', string='Boats')