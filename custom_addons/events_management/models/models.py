# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

class EventSpaceAmenity(models.Model):
    _name = 'event.space.amenity'
    _description = 'Event Space Amenity'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    

class EventSpace(models.Model):
    _name = 'event.space'
    _description = 'Event Space'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    image = fields.Image(string='Image')
    location = fields.Char(string='Location')
    capacity = fields.Integer(string='Capacity')
    description = fields.Text(string='Description')
    amenities = fields.Many2many('event.space.amenity', string='Amenities')
    price_per_hour = fields.Float(string='Price per Hour')
    is_available = fields.Boolean(string='Is Available', default=True)
    event_ids = fields.One2many('event.event', 'space_id', string='Events')
        
    pending_events_count = fields.Integer(string='Pending Events', compute='_compute_pending_events_count')
    next_event_date = fields.Datetime(string='Next Event Date', compute='_compute_next_event_date', store=True)
    
    @api.depends('event_ids')
    def _compute_next_event_date(self):
        for space in self:
            if space.event_ids:
                space.next_event_date = min(space.event_ids.mapped('start_date'))
            else:
                space.next_event_date = False
    
    @api.depends('event_ids')
    def _compute_pending_events_count(self):
        today = date.today()
        for space in self:
            space.pending_events_count = self.env['event.event'].search_count([
                ('space_id', '=', space.id),
                ('start_date', '>=', today)
            ])


class Event(models.Model):
    _name = 'event.event'
    _description = 'Event'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Event Name', required=True)
    start_date = fields.Datetime(string='Event Start Date', required=True)
    end_date = fields.Datetime(string='Event End Date', required=True)
    all_day = fields.Boolean(string='All Day')
    space_id = fields.Many2one('event.space', string='Event Space', required=True)
    organizer_id = fields.Many2one('res.partner', string='Organizer')
    is_private = fields.Boolean(string='Is Private', default=False)
    rental_agreement = fields.Binary(string='Rental Agreement')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft')
    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True)
    event_type = fields.Selection([
        ('wedding', 'Wedding'),
        ('other', 'Other')
    ], string='Event Type', required=True)
    event_type_details = fields.Char(string='Event Type Details')
    num_guests = fields.Integer(string='Number of Guests')
    private_event = fields.Boolean(string='Private Event')
    private_charge = fields.Boolean(string='Charge Patrons (Private)')
    commercial_event = fields.Boolean(string='Commercial Event')
    commercial_charge = fields.Boolean(string='Charge Patrons (Commercial)')
    commercial_charge_details = fields.Text(string='Commercial Charge Details')
    charity_event = fields.Boolean(string='Charity Event')
    charity_charge = fields.Boolean(string='Charge Patrons (Charity)')
    charity_name = fields.Char(string='Charity Name')
    charity_percentage = fields.Float(string='Charity Percentage')
    charity_confirmation = fields.Binary(string='Charity Confirmation Letter')
    tables_chairs_tents = fields.Boolean(string='Add Tables, Chairs & Tents')
    tables_required = fields.Integer(string='Tables Required')
    chairs_required = fields.Integer(string='Chairs Required')
    tents_required = fields.Integer(string='Tents Required')
    share_facilities = fields.Boolean(string='Share Facilities with Members')
    bar_service = fields.Selection([
        ('yours', 'Yours'),
        ('club', 'Club')
    ], string='Bar Drinks and Services')
    food_service = fields.Selection([
        ('yours', 'Yours'),
        ('club', 'Club')
    ], string='Food and Eats')
    entertainment_type = fields.Selection([
        ('dj', 'DJ'),
        ('live_band', 'Live Band'),
        ('na', 'N/A'),
        ('other', 'Other')
    ], string='Entertainment Type')
    entertainment_details = fields.Text(string='Entertainment Details')
    stage_platform = fields.Boolean(string='Stage/Platform Erected')
    marine_activities = fields.Boolean(string='Marine Activities Involved')
    
    is_organizer_current_company = fields.Boolean(
        string='Is Organizer Current Company',
        compute='_compute_is_organizer_current_company',
        store=True
    )
    
    def create_invoice(self):
        for event in self:
            if not event.invoice_id:
                partner = event.organizer_id
                # Create the invoice
                invoice = self.env['account.move'].create({
                    'move_type': 'out_invoice',
                    'partner_id': partner.id,
                    'invoice_date': fields.Date.today(),
                })
                # Link the invoice to the event
                event.invoice_id = invoice.id
                event.status = 'confirmed'

                # Open the invoice in form view
                return {
                    'name': 'Customer Invoice',
                    'view_mode': 'form',
                    'res_model': 'account.move',
                    'view_id': self.env.ref('account.view_move_form').id,
                    'type': 'ir.actions.act_window',
                    'res_id': invoice.id,
                }
                

    @api.depends('organizer_id')
    def _compute_is_organizer_current_company(self):
        for record in self:
            record.is_organizer_current_company = (record.organizer_id == self.env.company.partner_id)                