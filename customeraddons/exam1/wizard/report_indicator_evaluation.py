from odoo import fields, models, api,_
from datetime import date


class ReportIndicatorEvaluation(models.TransientModel):
    _name = 'report.indicator.evaluation'

    sale_team = fields.Many2many('crm.team', string="Nhóm bán hàng")
    month = fields.Selection([('1', 'January'), ('2', 'February'), ('3', 'March'),
        ('4', 'April'),('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
        ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')],
        string='Month', default=str(date.today().month), required=True)

    def btn_confirm(self):


        if self.month and self.sale_team:
            if self.month == str(date.today().month):
                self.month = str(date.today().month)
            sale_teams_id = self.sale_team.mapped('id')
            self.env['indicator.evaluation'].sudo().search([]).unlink()
            for id in sale_teams_id:
                self.env['indicator.evaluation'].sudo().create({
                    'sale_team': id,
                    'month': int(self.month)
                })

            context = {
                'name':  _("Detail Report"),
                'view_mode': 'tree',
                'res_model': 'indicator.evaluation',
                'type': 'ir.actions.act_window',
                'view_id': self.env.ref('exam1.indicator_evaluation_tree_view').id,
                'target': 'current',
                'domain': [('sale_team', 'in', sale_teams_id), ('month', '=', int(self.month))],
                'context': {'create': False, 'edit': False, 'delete': False}
            }

        else:
            context = {
                'name':  _("Detail Report"),
                'view_mode': 'tree',
                'res_model': 'indicator.evaluation',
                'type': 'ir.actions.act_window',
                'view_id': self.env.ref('exam1.indicator_evaluation_tree_view').id,
                'target': 'current',
                'context': {'create': False, 'edit': False, 'delete': False}
            }
        return context