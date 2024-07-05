from odoo import http
from odoo.http import request

class MemberApplicationController(http.Controller):

    @http.route('/member/application', type='http', auth='public', website=True)
    def member_application_form(self, **kwargs):
        countries = request.env['res.country'].search([])
        return request.render('yc_member_application.member_application_form', {
            'countries': countries
        })

    @http.route('/member/application/submit', type='http', auth='public', methods=['POST'], website=True)
    def member_application_submit(self, **post):
        vals = {
            'first_name': post.get('first_name'),
            'last_name': post.get('last_name'),
            'other_names': post.get('other_names'),
            'email': post.get('email'),
            'profile_picture': post.get('profile_picture'),
            'date_of_birth': post.get('date_of_birth'),
            'street_address': post.get('street_address'),
            'city': post.get('city'),
            'country_id': int(post.get('country_id')),
            'home_number': post.get('home_number'),
            'office_number': post.get('office_number'),
            'mobile_number': post.get('mobile_number'),
            'marital_status': post.get('marital_status'),
            'spouse_name': post.get('spouse_name'),
            'has_kids': post.get('has_kids') == 'on',
            # Handle children, business data, documents, boats, other memberships, etc.
        }
        request.env['member.application'].sudo().create(vals)
        return request.redirect('/member/application/thankyou')
