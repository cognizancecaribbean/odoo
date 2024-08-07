from odoo import models, fields, api


class BoatSpecification(models.Model):
    _name = 'boatyard.boat.specification'
    _description = 'Boat Specification'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Boat Name")
    boat_length = fields.Float(string="Boat Length")
    boat_beam = fields.Float(string="Boat Beam")
    boat_draft = fields.Float(string="Boat Draft")
    hull_material = fields.Char(string="Hull Material")
    boat_colors = fields.Char(string="Boat Colors")
    boat_mass = fields.Float(string="Boat Mass")
    boat_water_capacity = fields.Float(string="Water Capacity")
    boat_fuel_capacity = fields.Float(string="Fuel Capacity")
    boat_cellular = fields.Char(string="Cellular")
    boat_call_sign = fields.Char(string="Call Sign")
    is_original_owner = fields.Boolean(string="Is Original Owner")
    original_owner = fields.Char(string="Original Owner")
    original_owner_street = fields.Char(string="Original Owner Street Address")
    original_owner_city = fields.Char(string="Original Owner City")
    original_owner_country = fields.Many2one('res.country', string='Original Owner Country', help='Select Country')
    original_owner_date_purchased = fields.Date(string="Original Owner Date Purchased")
    place_manufactured = fields.Selection([
        ('local', 'Local'),
        ('foreign', 'Foreign')
    ], string="Place Manufactured", default='foreign')
    year_manufactured = fields.Integer(string="Year Manufactured")
    manufacturer_name = fields.Char(string="Manufacturer Name")
    country_imported_from = fields.Many2one('res.country', string='Country Imported From', help='Select Country')
    date_imported = fields.Date(string="Date Imported")
    transportation_mode = fields.Char(string="Transportation Mode")
    boat_picture = fields.Binary(string="Boat Picture")
    member_boat_id = fields.Many2one('members.management.boat', string="Boat", required=True)


class BoatDocument(models.Model):
    _name = 'boatyard.boat.document'
    _description = 'Boat Document'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    boat_id = fields.Many2one('boatyard.boat.specification', string="Boat", required=True)
    name = fields.Char(string="Document Name")
    file = fields.Binary(string="File")
    expires = fields.Boolean(string="Expires")
    expiry_date = fields.Date(string="Expiry Date")


class BoatEngine(models.Model):
    _name = 'boatyard.boat.engine'
    _description = 'Boat Engine'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    boat_id = fields.Many2one('boatyard.boat.specification', string="Boat", required=True)
    make = fields.Char(string="Engine Make")
    model = fields.Char(string="Engine Model")
    engine_type = fields.Selection([
        ('outboard', 'Outboard'),
        ('inboard', 'Inboard'),
        ('stern_drive', 'Stern Drive'),
        ('jet_drive', 'Jet Drive')
    ], string="Engine Type")
    horsepower = fields.Float(string="Horsepower")
    serial_number = fields.Char(string="Serial Number")


class BoatDevice(models.Model):
    _name = 'boatyard.boat.device'
    _description = 'Boat Device'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    boat_id = fields.Many2one('boatyard.boat.specification', string="Boat", required=True)
    make = fields.Char(string="Make")
    model = fields.Char(string="Model")
    device_type = fields.Selection([
        ('vhf_radio', 'VHF Radio'),
        ('hf_ssb_radio', 'HF/SSB Radio'),
        ('gps', 'Global Positioning System'),
        ('echo_sounder', 'Echo Sounder'),
        ('other', 'Other Devices')
    ], string="Type")
    serial_number = fields.Char(string="Serial Number")
    description = fields.Text(string="Description")


class BoatSpace(models.Model):
    _name = 'boatyard.boat.space'
    _description = 'Boat Space'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")
    length = fields.Float(string="Length")
    width = fields.Float(string="Width")
    height = fields.Float(string="Height")
    space_type = fields.Selection([
        ('boat_slip', 'Boat Slip'),
        ('dry_dock', 'Dry Dock Space'),
        ('repairs_shed', 'Repairs Shed Space')
    ], string="Space Type")
    is_available = fields.Boolean(string='Is Available', default=True)


class BoatSpaceBooking(models.Model):
    _name = 'boatyard.boat.space.booking'
    _description = 'Boat Space Booking'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    boat_id = fields.Many2one('members.management.boat', string="Boat", required=True)
    space_id = fields.Many2one('boatyard.boat.space', string="Boat Space", required=True)
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done')
    ], string='Status', default='draft')
    
    def name_get(self):
        result = []
        for record in self:
            name = record.boat_id.name
            result.append((record.id, name))
        return result    
    


class BoatMovement(models.Model):
    _name = 'boatyard.boat.movement'
    _description = 'Boat Movement'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    boat_id = fields.Many2one('boatyard.boat.specification', string="Boat", required=True)
    notice_type = fields.Selection([
        ('boat_in', 'Boat In'),
        ('boat_out', 'Boat Out')
    ], string="Activity Notice Type")
    estimated_time = fields.Datetime(string="Estimated Activity Time")
    actual_time = fields.Datetime(string="Actual Activity Time")
