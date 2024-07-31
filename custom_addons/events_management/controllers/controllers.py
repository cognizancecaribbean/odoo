# -*- coding: utf-8 -*-
# from odoo import http


# class EventsManagement(http.Controller):
#     @http.route('/events_management/events_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/events_management/events_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('events_management.listing', {
#             'root': '/events_management/events_management',
#             'objects': http.request.env['events_management.events_management'].search([]),
#         })

#     @http.route('/events_management/events_management/objects/<model("events_management.events_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('events_management.object', {
#             'object': obj
#         })

