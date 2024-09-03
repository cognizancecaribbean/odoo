from odoo import models, fields, api

class Citizen(models.Model):
    _name = 'citizen'
    _description = 'Citizen'

    # Adding citizen-specific fields
    ebc_system_id = fields.Char(string="EBC System ID", help="Link to voter records")
    national_id_no = fields.Char(string="National ID No.")
    voter_ids = fields.One2many('voter', 'citizen_id', string="Voter Records")

    # Adding citizen-specific computed fields or methods if needed
    @api.depends('voter_ids')
    def _compute_voter_count(self):
        for record in self:
            record.voter_count = len(record.voter_ids)

    voter_count = fields.Integer(string="Voter Count", compute="_compute_voter_count")
    
    contact_id = fields.Many2one('res.partner', string="Contact", ondelete='restrict', required=True, index=True)

    _sql_constraints = [
        ('contact_uniq', 'unique(contact_id)', 'A contact record is already linked to this citizen.'),
    ]