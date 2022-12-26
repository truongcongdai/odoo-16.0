from odoo import fields, api, models

class InheritSaleOrder(models.Model):
    _inherit = 'sale.order'
    plan_sale_order_id = fields.Many2one('plan.sale.order', string='Plan Sale Order')

    # Ghi đè kiểm tra kế hoạch đã thêm và kế hoạch đã được phê duyệt
    def action_confirm(self):
        if self.plan_sale_order_id and self.plan_sale_order_id.is_confirm == True:
            return super(InheritSaleOrder, self).action_confirm()
        else:
            raise models.ValidationError('The business plan has not been added or approved yet')