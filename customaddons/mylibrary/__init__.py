from . import models
# from . import wizard
#
# from odoo import SUPERUSER_ID, fields, api
# def add_book_hook(cr, registry):
#     env = api.Environment(cr, SUPERUSER_ID , {})
#     book_data1 = {'name':'Book 1', 'date_release':fields.Date.today()}
#     book_data2 = {'name':'Book 2', 'date_release':fields.Date.today()}
#     env['library.book'].create([book_data1, book_data2])