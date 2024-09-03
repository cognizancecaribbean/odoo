from odoo import models, fields

class Election(models.Model):
    _name = 'election'
    _description = 'Election'

    title = fields.Char(string="Election Title", required=True)
    year = fields.Integer(string="Election Year", required=True)
    election_type = fields.Selection([('general', 'General'), ('local', 'Local')], string="Election Type")
    voter_ids = fields.One2many('voter', 'election_id', string="Voters")
