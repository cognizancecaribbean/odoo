from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    office_phone = fields.Char(string='Office Phone')
    postal_code = fields.Char(string='Postal Code')
    is_citizen = fields.Boolean(string="Is a Citizen", compute='_compute_is_citizen')
    citizen_ids = fields.One2many('citizen', 'contact_id', string="Citizens")

    @api.depends('citizen_ids')
    def _compute_is_citizen(self):
        for record in self:
            record.is_citizen = bool(record.citizen_ids)    