# -*- coding: utf-8 -*-
# from odoo import http


# class CmpAdmin(http.Controller):
#     @http.route('/cmp_admin/cmp_admin', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cmp_admin/cmp_admin/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cmp_admin.listing', {
#             'root': '/cmp_admin/cmp_admin',
#             'objects': http.request.env['cmp_admin.cmp_admin'].search([]),
#         })

#     @http.route('/cmp_admin/cmp_admin/objects/<model("cmp_admin.cmp_admin"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cmp_admin.object', {
#             'object': obj
#         })

