# -*- coding: utf-8 -*-

from odoo import http, fields
from odoo.http import request
import base64
from datetime import datetime
import tempfile
import subprocess


class ArtisanRegistrationController(http.Controller):

    @http.route(['/artisan/register'], type='http', auth="public", website=True)
    def artisan_registration_form(self, **kw):
        return request.render('artisan_management.artisan_registration_template')

    @http.route('/artisan/register/submit', type='http', auth='public', website=True, csrf=False)
    def submit_artisan_registration(self, **post):
        # Handle file uploads
        national_id = post.get('national_id')
        birth_certificate = post.get('birth_certificate')
        business_certificate = post.get('business_certificate')

        national_id_filename = national_id.filename if national_id else False
        birth_certificate_filename = birth_certificate.filename if birth_certificate else False
        business_certificate_filename = business_certificate.filename if business_certificate else False

        if national_id:
            national_id = base64.b64encode(national_id.read())
        if birth_certificate:
            birth_certificate = base64.b64encode(birth_certificate.read())
        if business_certificate:
            business_certificate = base64.b64encode(business_certificate.read())

        # Create a new Artisan Registration record
        new_registration = request.env['artisan.registration'].sudo().create({
            'first_name': post.get('first_name'),
            'last_name': post.get('last_name'),
            'gender': post.get('gender'),
            'email': post.get('email'),
            'home_phone': post.get('home_phone'),
            'mobile': post.get('mobile'),
            'id_type': post.get('id_type'),
            'id_number': post.get('id_number'),
            'national_id': national_id,
            'national_id_filename': national_id_filename,
            'birth_certificate': birth_certificate,
            'birth_certificate_filename': birth_certificate_filename,
            'business_name': post.get('business_name'),
            'business_summary': post.get('business_summary'),
            'street_address': post.get('street_address'),
            'city_town': post.get('city_town'),
            'country': post.get('country'),
            'is_registered': post.get('is_registered'),  # Assuming this is the field for registered/unregistered status
            'business_registration_date': post.get('business_registration_date'),
            'business_registration_number': post.get('business_registration_number'),
            'business_certificate': business_certificate,
            'business_certificate_filename': business_certificate_filename,
            'bir_no': post.get('bir_no'),
            'legal_structure': post.get('legal_structure'),
            'website': post.get('website'),
            'facebook': post.get('facebook'),
            'twitter': post.get('twitter'),
            'instagram': post.get('instagram'),
            'linkedin': post.get('linkedin'),
        })
        
        # Log the registration activity
        request.env['artisan.activity.log'].sudo().create({
            'activity_type': 'registration',
            'artisan_id': new_registration.id,
            'activity_date': fields.Datetime.now(),
        })

        return request.render('artisan_management.registration_success_template')


class ArtisanDashboardController(http.Controller):

    @http.route('/artisan_dashboard/get_totals', type='json', auth='user')
    def get_totals(self):
        total_artisans = request.env['artisan.registration'].get_total_artisans()
        total_pending = request.env['artisan.registration'].get_total_pending()
        total_vetting = request.env['artisan.registration'].get_total_vetting()
        total_approved = request.env['artisan.registration'].get_total_approved()
        total_denied = request.env['artisan.registration'].get_total_denied()
        totals_by_tag = request.env['artisan.registration'].get_totals_by_tag()

        return {
            'total_artisans': total_artisans,
            'total_pending': total_pending,
            'total_vetting': total_vetting,
            'total_approved': total_approved,
            'total_denied': total_denied,
            'totals_by_tag': totals_by_tag,
        }
        
    @http.route('/artisan_dashboard/get_ytd_totals', type='json', auth='user')
    def get_ytd_totals(self):
        current_year = datetime.now().year
        start_date = datetime(current_year, 1, 1)
        end_date = datetime(current_year, 12, 31)
        logs = request.env['artisan.activity.log'].search([
            ('activity_date', '>=', start_date),
            ('activity_date', '<=', end_date)
        ])
        ytd_registrations = logs.filtered(lambda log: log.activity_type == 'registration')
        ytd_approvals = logs.filtered(lambda log: log.activity_type == 'approval')
        ytd_denials = logs.filtered(lambda log: log.activity_type == 'denial')
        
        return {
            'ytd_registrations_total': len(ytd_registrations),
            'ytd_approvals_total': len(ytd_approvals),
            'ytd_denials_total': len(ytd_denials),
            'current_year': current_year,
            'start_date': start_date,
            'end_date': end_date,
        }        
              
                          