# -*- coding: utf-8 -*-
# from odoo import http


# class BoatyardManagement(http.Controller):
#     @http.route('/boatyard_management/boatyard_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/boatyard_management/boatyard_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('boatyard_management.listing', {
#             'root': '/boatyard_management/boatyard_management',
#             'objects': http.request.env['boatyard_management.boatyard_management'].search([]),
#         })

#     @http.route('/boatyard_management/boatyard_management/objects/<model("boatyard_management.boatyard_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('boatyard_management.object', {
#             'object': obj
#         })

