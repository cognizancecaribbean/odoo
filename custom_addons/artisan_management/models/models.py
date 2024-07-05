from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, date

class ArtisanTag(models.Model):
    _name = 'artisan.tag'
    _description = 'Artisan Tag'

    name = fields.Char(string='Tag Name', required=True)
    action_id = fields.Many2one('ir.actions.act_window', string='Associated Action', ondelete='cascade')

    @api.model
    def create(self, vals):
        record = super(ArtisanTag, self).create(vals)
        record._create_or_update_action()
        return record

    def write(self, vals):
        res = super(ArtisanTag, self).write(vals)
        if 'name' in vals:
            self._create_or_update_action()
        return res

    def unlink(self):
        actions = self.mapped('action_id')
        res = super(ArtisanTag, self).unlink()
        if actions:
            actions.sudo().unlink()
        return res

    def _create_or_update_action(self):
        action_model = self.env['ir.actions.act_window']
        data_model = self.env['ir.model.data']

        for tag in self:
            action_name = f"action_artisans_with_tag_{tag.id}"
            action_xmlid = f"artisan_management.{action_name}"

            existing_action = action_model.search([('id', '=', tag.action_id.id)], limit=1)
            action_vals = {
                'name': f'Artisans with {tag.name}',
                'type': 'ir.actions.act_window',
                'res_model': 'artisan.registration',
                'view_mode': 'tree,form',
                'domain': [('tags_ids', '=', tag.id)],
                'context': {'search_default_tag_ids': tag.id},
                'target': 'current',
            }

            if existing_action:
                existing_action.sudo().write(action_vals)
                # Update the ir.model.data record
                data_model.sudo().search([('res_id', '=', existing_action.id), ('model', '=', 'ir.actions.act_window')]).write({
                    'module': 'artisan_management',
                    'name': action_name,
                })
            else:
                new_action = action_model.sudo().create(action_vals)
                tag.sudo().write({'action_id': new_action.id})
                # Create a new ir.model.data record
                data_model.sudo().create({
                    'name': action_name,
                    'module': 'artisan_management',
                    'model': 'ir.actions.act_window',
                    'res_id': new_action.id,
                    'noupdate': True,
                })
                
    @api.model
    def update_actions_for_existing_tags(self):
        tag_model = self.env['artisan.tag']
        action_model = self.env['ir.actions.act_window']
        data_model = self.env['ir.model.data']

        # Fetch all existing tags
        tags = tag_model.search([])

        for tag in tags:
            action_name = f"action_artisans_with_tag_{tag.id}"

            # Check if an action already exists for the tag
            existing_action = action_model.search([('id', '=', tag.action_id.id)], limit=1)

            action_vals = {
                'name': f'Artisans with {tag.name}',
                'type': 'ir.actions.act_window',
                'res_model': 'artisan.registration',
                'view_mode': 'tree,form',
                'domain': [('tags_ids', '=', tag.id)],
                'context': {'search_default_tag_ids': tag.id},
                'target': 'current',
            }

            if existing_action:
                # Update existing action
                existing_action.sudo().write(action_vals)
                # Update the corresponding ir.model.data record
                data_model.sudo().search([('res_id', '=', existing_action.id), ('model', '=', 'ir.actions.act_window')]).write({
                    'module': 'artisan_management',  # or your module name
                    'name': action_name,
                })
            else:
                # Create new action
                new_action = action_model.sudo().create(action_vals)
                # Associate the new action with the tag
                tag.sudo().write({'action_id': new_action.id})
                # Create a new ir.model.data record
                data_model.sudo().create({
                    'name': action_name,
                    'module': 'artisan_management',  # or your module name
                    'model': 'ir.actions.act_window',
                    'res_id': new_action.id,
                })

        # Return client action for notification
        return True             


class ArtisanRegistration(models.Model):
    _name = 'artisan.registration'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Artisan Registration'

    first_name = fields.Char(string="First Name", required=True, tracking=True)
    last_name = fields.Char(string="Last Name", required=True, tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", required=True, tracking=True)
    email = fields.Char(string="Email Address", required=True, tracking=True)
    home_phone = fields.Char(string="Home Phone", required=True, tracking=True)
    mobile = fields.Char(string="Mobile", required=True, tracking=True)
    id_type = fields.Selection([('id_card', 'ID Card'), ('dp', 'Drivers Permit'), ('passport', 'Passport')], string="ID Type", required=True, tracking=True)
    id_number = fields.Char(string="ID Number", required=True, tracking=True)
    national_id = fields.Binary(string="ID Copy (Upload)", required=True, attachment=True)
    national_id_filename = fields.Char(string='National ID Filename')
    birth_certificate = fields.Binary(string="Birth Certificate (Upload)", required=True, attachment=True)
    birth_certificate_filename = fields.Char(string='Birth Certificate Filename')
    
    business_name = fields.Char(string="Business Name", required=True, tracking=True)
    business_summary = fields.Text(string="Business Summary", required=True, tracking=True)
    street_address = fields.Char(string="Street Address", required=True, tracking=True)
    city_town = fields.Char(string="City / Town", required=True, tracking=True)
    country = fields.Selection([('trinidad', 'Trinidad'), ('tobago', 'Tobago')], string="Country", required=True, tracking=True)
    is_registered = fields.Selection([('registered', 'Registered'), ('unregistered', 'Unregistered')], string="Business Registration", default='unregistered', required=True, tracking=True)
    business_registration_date = fields.Date(string='Business Registration Date', tracking=True)
    business_registration_number = fields.Char(string="Business Registration Number", tracking=True)
    business_certificate = fields.Binary(string="Business Certificate Copy (Upload)", attachment=True)
    business_certificate_filename = fields.Char(string='Business Certificate Filename')
    bir_no = fields.Char(string="BIR Number")
    legal_structure = fields.Selection([
        ('sole', 'Sole Proprietorship'), 
        ('partnership', 'Partnership'), 
        ('llc', 'LLC'), 
        ('corporation', 'Corporation')
    ], string='Legal Structure', tracking=True)
    website = fields.Char(string="Website", tracking=True)
    facebook = fields.Char(string="Facebook", tracking=True)
    twitter = fields.Char(string="Twitter", tracking=True)
    instagram = fields.Char(string="Instagram", tracking=True)
    linkedin = fields.Char(string="LinkedIn", tracking=True)
    state = fields.Selection([('pending', 'Pending'), ('vetting', 'Vetting'), ('approved', 'Approved'), ('denied', 'Not Approved')], default='pending', string="Status", tracking=True)
    user_id = fields.Many2one('res.users', string='User', readonly=True)
    tags_ids = fields.Many2many('artisan.tag', string='Tags')
    artisan_id = fields.Char(string="Artisan ID", readonly=True)
    
    # Computed name field
    name = fields.Char(string='Name', compute='_compute_name', store=True)
    
    # Constraints
    _sql_constraints = [
        ('email_unique', 'UNIQUE(email)', 'Your email must be unique!')
    ]

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.first_name} {record.last_name}"
            
    def write(self, vals):
        res = super(ArtisanRegistration, self).write(vals)
        for record in self:
            if 'first_name' in vals or 'last_name' in vals or 'email' in vals:
                if record.user_id:
                    user_vals = {
                        'name': f"{record.first_name} {record.last_name}",
                        'login': record.email,
                        'email': record.email,
                    }
                    record.user_id.sudo().write(user_vals)
                    record.user_id.partner_id.sudo().write(user_vals)
        return res

    def action_vet(self):
        self.state = 'vetting'

    def action_approve(self):  
        if not self.artisan_id:
            self.artisan_id = self._generate_artisan_id()      
        user = self.create_artisan_profile()
        self.send_acceptance_email(user)
        self.state = 'approved'
        self.log_activity('approval')
        
    def _generate_artisan_id(self):
        year = datetime.now().year
        artisan_id = f"{year}-{self.id}"
        return artisan_id

    def action_deny(self):
        self.state = 'denied'
        self.log_activity('denial')
        
    def action_revert_to_vetting(self):
        self.state = 'vetting'
        self.log_activity('reverted_to_vetting')
        
    def action_send_acceptance_email(self):
        user = self.user_id
        if user:
            self.send_acceptance_email(user)       

    def create_artisan_profile(self):
        user = self.env['res.users'].sudo().create({
            'name': f"{self.first_name} {self.last_name}",
            'login': self.email,
            'email': self.email,
            'partner_id': self.env['res.partner'].create({
                'name': f"{self.first_name} {self.last_name}",
                'email': self.email,
            }).id,
            'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])],  # Adding the user to the portal group
        })
        user.partner_id.signup_prepare()  # Prepare the signup token
        return user

    def send_acceptance_email(self, user):
            template = self.env.ref('auth_signup.set_password_email')  # Get the default signup template
            self.env['mail.template'].browse(template.id).send_mail(user.id, force_send=True)
            
    def log_activity(self, activity_type):
        self.env['artisan.activity.log'].create({
            'activity_type': activity_type,
            'artisan_id': self.id,
            'activity_date': fields.Datetime.now(),
        })                 
            
    @api.model
    def get_total_artisans(self):
        return self.search_count([])
    
    @api.model
    def get_total_pending(self):
        return self.search_count([('state', '=', 'pending')])    

    @api.model
    def get_total_vetting(self):
        return self.search_count([('state', '=', 'vetting')])

    @api.model
    def get_total_approved(self):
        return self.search_count([('state', '=', 'approved')])

    @api.model
    def get_total_denied(self):
        return self.search_count([('state', '=', 'denied')])

    @api.model
    def get_totals_by_tag(self):
        tag_model = self.env['artisan.tag']
        tags = tag_model.search([])
        totals = []

        for tag in tags:
            total = self.search_count([('tags_ids', 'in', [tag.id])])
            totals.append({
                'tag_name': tag.name,
                'count': total,
                'action_id': tag.action_id.id if tag.action_id else False
            })
            
        # Sort totals list alphabetically by tag_name
        totals_sorted = sorted(totals, key=lambda x: x['tag_name'])

        return totals_sorted             
    
    
class ArtisanActivityLog(models.Model):
    _name = 'artisan.activity.log'
    _description = 'Activity Log for Artisan Actions'

    activity_type = fields.Selection([
        ('registration', 'Registration'),
        ('approval', 'Approval'),
        ('denial', 'Denial'),
        ('reverted_to_vetting', 'Revert To Vetting')
    ], required=True)
    artisan_id = fields.Many2one('artisan.registration', string='Artisan', required=True)
    activity_date = fields.Datetime(string='Activity Date', default=fields.Datetime.now, required=True)        
    
    # Computed field to display in tree view or other places
    name = fields.Char('Name', compute='_compute_name', store=True)

    @api.depends('artisan_id')
    def _compute_name(self):
        for record in self:
            if record.artisan_id:
                record.name = record.artisan_id.name
            else:
                record.name = "Unnamed Artisan"                  
    
    
class ArtisanTraining(models.Model):
    _name = 'artisan.training'
    _description = 'Artisan Training'

    name = fields.Char(string="Training Program", required=True)
    date = fields.Date(string="Date")
    artisan_id = fields.Many2one('artisan.registration', string="Artisan")
    

class ArtisanProduct(models.Model):
    _name = 'artisan.product'
    _description = 'Artisan Product'

    name = fields.Char(string="Product Name", required=True)
    description = fields.Text(string="Product Description")
    price = fields.Float(string="Price")
    artisan_id = fields.Many2one('artisan.registration', string="Artisan")


class ArtisansByStateReport(models.AbstractModel):
    _name = 'report.artisan_management.report_artisans_by_state'

    @api.model
    def _get_report_values(self, docids=None, data=None):
        # Fetch data for the report
        if not docids:
            artisans = self.env['artisan.registration'].search([])
        else:
            artisans = self.env['artisan.registration'].browse(docids)
        print("All Artisans:", artisans) # Check list
        
        artisans_by_state = {}

        for artisan in artisans:
            state = artisan.state
            if state not in artisans_by_state:
                artisans_by_state[state] = []
            artisans_by_state[state].append(artisan)
            
        print("Artisans grouped by state:", artisans_by_state) # Check Artisans by State

        # Prepare report values
        report_values = {
            'doc_ids': docids,
            'doc_model': 'artisan.registration',
            'artisans_by_state': artisans_by_state,
        }
        print("Final Report Content:", report_values) # Check final report data

        return report_values
    

class ArtisansByActivityTypeReport(models.AbstractModel):
    _name = 'report.artisan_management.artisans_by_activity_type'
    _description = 'Artisans by Activity Type Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        print('Entering _get_report_values')
        current_year = datetime.now().year
        start_date = datetime(current_year, 1, 1)
        end_date = datetime(current_year, 12, 31)
        
        activities = self.env['artisan.activity.log'].search([
            ('activity_date', '>=', start_date),
            ('activity_date', '<=', end_date)
        ])
        print("Activities:", activities)

        ytd_activities = {}
        for activity in activities:
            if activity.activity_type not in ytd_activities:
                ytd_activities[activity.activity_type] = []
            ytd_activities[activity.activity_type].append({
                'date': activity.activity_date,
                'name': activity.artisan_id.name,
                'email': activity.artisan_id.email,
            })

        print("YTD Activities:", ytd_activities)

        report_values = {
            'doc_ids': docids,
            'doc_model': 'artisan.activity.log',
            'ytd_activities': ytd_activities,
        }

        print("Final Report Values:", report_values)
        return report_values