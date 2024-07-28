from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_member = fields.Boolean(string='Is a Member', readonly=True)