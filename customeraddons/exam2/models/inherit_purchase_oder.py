from odoo import models,fields

class InheritPurchaseOder(models.Model):
    _inherit = 'purchase.order'

    department = fields.Many2one('hr.department', required=True, string='Department')

    def button_confirm(self):
        current_user = self.env.uid
        employees = self.env['limit.purchase.order'].search([('name', '=', current_user)])
        employee = employees.mapped('order_limit')
        print(employees)
        print('.........',current_user  )

