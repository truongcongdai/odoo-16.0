from odoo import models, fields
from odoo.exceptions import UserError
from odoo.tools.translate import _


class SSaleOrder(models.Model):
    _inherit = 'sale.order'

    plan_sale_order = fields.Many2one('plan.sale.order', string='Plan sale order')
    # ondelete='cascade',index=True, copy=False, invisible=True

    plan_sale_order_id = fields.One2many('plan.sale.order', 'quotation', string='Order')
    new_quotation = fields.Many2one(related='plan_sale_order_id.quotation')
    new_state = fields.Selection(related='plan_sale_order_id.state')

    # Confirm button in Sale orders
    def action_confirm(self):
        res = super(SSaleOrder, self).action_confirm()
        if not self.new_quotation or self.new_state != 'approve':
            raise models.ValidationError('Not available/Not approved plan sale order')
        return res
