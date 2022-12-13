from odoo import models, fields, api

class ReportPurchase(models.TransientModel):
    _name = "report.purchase"
    _description = "Report Purchase"

    month = fields.Selection([('1','January'), ('2','February'), ('3','March'),
                              ('4','April'), ('5', 'May'), ('6','June'), ('7','July'),
                              ('8','August'), ('9','September'), ('10','October'), ('11','November'), ('12','December')],
                             default=str(fields.Datetime.today().month), string='Month')
    department = fields.Many2many('hr.department', string="Department")

