from odoo import models, fields, api
class IndicatorEvaluationReport(models.Model):
    _name = 'indicator.evaluation'

    sale_team = fields.Many2one('crm.team', string="Nhóm bán hàng")
    actual_revenue = fields.Float(string="Doanh thu thực tế",compute="_compute_actual_revenue", store=False)
    month = fields.Integer('Month', store=True)
    revenue_targets = fields.Float(string="Chỉ tiêu doanh thu", compute="_compute_revenue_targets", store=True)

    def _compute_actual_revenue(self):
        for rec in self:
            if rec.sale_team:
                amount_untaxed_opportunity = self.env['sale.order'].search(
                    [('team_id', 'in', rec.sale_team.mapped('id'))])
                amount_untaxed = amount_untaxed_opportunity.mapped('amount_untaxed')
                rec.actual_revenue = sum(amount_untaxed)

    # Get value month revenue to month of report
    @api.depends('month')
    def _compute_revenue_targets(self):
        for rec in self:
            if rec.month:
                month_sales_result = self.env['crm.team'].search([('id', 'in', rec.sale_team.mapped('id'))])
                month_sales = month_sales_result.mapped(lambda res: (res.january, res.february,
                                                                     res.march, res.april, res.may,
                                                                     res.june, res.july, res.august,
                                                                     res.september, res.october,
                                                                     res.november, res.december))
                rec.revenue_targets = month_sales[0][rec.month - 1]
