from odoo import models, fields

class Voter(models.Model):
    _name = 'voter'
    _description = 'Voter'

    election_id = fields.Many2one('election', string="Election")
    system_id = fields.Char(string="System ID")
    name = fields.Char(string="Name")
    address_id = fields.Many2one('address', string="Address")
    citizen_id = fields.Many2one('citizen', string="Citizen", required=True)
