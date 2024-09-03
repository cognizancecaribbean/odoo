from odoo import models, fields

class Election(models.Model):
    _name = 'election'
    _description = 'Election'

    name = fields.Char(string="Election Title", required=True)
    election_type = fields.Selection([('general', 'General'), ('local', 'Local'), {'tha', 'THA'}], string="Election Type")
    voter_ids = fields.One2many('voter', 'election_id', string="Voters")
    election_date = fields.Date(string="Election Date", required=True)