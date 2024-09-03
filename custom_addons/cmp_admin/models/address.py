# models/address.py
from odoo import models, fields, api

class ParliamentaryElectoralDistrict(models.Model):
    _name = 'parliamentary.electoral.district'
    _description = 'Parliamentary Electoral District'

    ped_name = fields.Char(string='PED Name', required=True)
    # Computed name field
    name = fields.Char(string='Name', compute='_compute_name', store=True)
    
    @api.depends('ped_name')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.ped_name}"


class ElectoralDistrict(models.Model):
    _name = 'electoral.district'
    _description = 'Electoral District'

    ed_name = fields.Char(string='ED Name', required=True)
    corporation_id = fields.Many2one('regional.corporation', string='Regional Corporation', required=True)


class RegionalCorporation(models.Model):
    _name = 'regional.corporation'
    _description = 'Regional Corporation'

    corporation_name = fields.Char(string='Corporation Name', required=True)
    # Computed name field
    name = fields.Char(string='Name', compute='_compute_name', store=True)
    
    @api.depends('corporation_name')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.corporation_name}"
    

class PollingDistrict(models.Model):
    _name = 'polling.district'
    _description = 'Polling District'

    pd_number = fields.Char(string='PD Number', required=True)
    ped_id = fields.Many2one('parliamentary.electoral.district', string='Parliamentary Electoral District', required=True)
    ed_id = fields.Many2one('electoral.district', string='Electoral District', required=True)


class Address(models.Model):
    _name = 'address'
    _description = 'Address'

    building = fields.Char(string='Building')
    apt = fields.Char(string='Apartment')
    street_id = fields.Many2one('street', string='Street', required=True)
    pd_id = fields.Many2one('polling.district', string='Polling District', required=True)


class Street(models.Model):
    _name = 'street'
    _description = 'Street'

    name = fields.Char(string='Street Name', required=True)

