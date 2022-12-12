from odoo import models,fields,api

class InheritHrDepartment(models.Model):
    _inherit = 'hr.department'

    spending_limit_month = fields.Float(string="Spending Limit Month")
