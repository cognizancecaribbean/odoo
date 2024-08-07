from odoo import models, fields, api

class ResPartnerBoat(models.Model):
    _name = 'members.management.boat'
    _description = 'Member Boat'

    name = fields.Char(string='Boat Name', required=True)
    size = fields.Char(string='Boat Size')
    engine = fields.Char(string='Boat Engine(s)')
    partner_ids = fields.Many2many('res.partner', string='Owners')
    member_ids = fields.Many2many('members.management.member', string='Members', compute='_compute_member_ids', store=True)

    @api.depends('partner_ids')
    def _compute_member_ids(self):
        for record in self:
            members = self.env['members.management.member'].search([('partner_id', 'in', record.partner_ids.ids)])
            record.member_ids = members

    @api.model
    def create(self, vals):
        if 'partner_ids' in vals:
            # Ensure partner_ids is a list of IDs
            vals['partner_ids'] = [(6, 0, vals.get('partner_ids', []))]
        return super(ResPartnerBoat, self).create(vals)

    def write(self, vals):
        if 'partner_ids' in vals:
            # Ensure partner_ids is a list of IDs
            vals['partner_ids'] = [(6, 0, vals.get('partner_ids', []))]
        return super(ResPartnerBoat, self).write(vals)
