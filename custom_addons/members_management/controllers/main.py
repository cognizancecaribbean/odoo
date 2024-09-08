from odoo import http
from odoo.http import request


class ApplicantDashboardController(http.Controller):

    @http.route('/applicants_dashboard/get_totals', type='json', auth='user')
    def get_totals(self):
        total_applicants = request.env['members.management.member'].get_total_applicants()
        total_new_applicants = request.env['members.management.member'].get_total_new_applicants()
        total_acknowledged_applicants = request.env['members.management.member'].get_total_acknowledged_applicants()
        total_interview_applicants = request.env['members.management.member'].get_total_interview_applicants()
        total_followup_applicants = request.env['members.management.member'].get_total_followup_applicants()
        total_welcomed_applicants = request.env['members.management.member'].get_total_welcomed_applicants()
        total_orientation_applicants = request.env['members.management.member'].get_total_orientation_applicants()
        total_applicants_sent_bylaws = request.env['members.management.member'].get_total_sent_bylaws_applicants()
        total_applicants_sent_quotes = request.env['members.management.member'].get_total_sent_quote_applicants()
        total_applicants_signed_quotes = request.env['members.management.member'].get_total_signed_quote_applicants()
        total_applicants_sub_initialized = request.env['members.management.member'].get_total_sub_initialized_applicants()

        return {
            'total_applicants': total_applicants,
            'total_new_applicants': total_new_applicants,
            'total_acknowledged_applicants': total_acknowledged_applicants,
            'total_interview_applicants': total_interview_applicants,
            'total_followup_applicants': total_followup_applicants,
            'total_welcomed_applicants': total_welcomed_applicants,
            'total_orientation_applicants': total_orientation_applicants,
            'total_applicants_sent_bylaws': total_applicants_sent_bylaws,
            'total_applicants_sent_quotes': total_applicants_sent_quotes,
            'total_applicants_signed_quotes': total_applicants_signed_quotes,
            'total_applicants_sub_initialized': total_applicants_sub_initialized
        }