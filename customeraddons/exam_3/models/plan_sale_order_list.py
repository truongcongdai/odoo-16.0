from odoo import models, fields


class PlanSaleOrderList(models.Model):
    _name = 'plan.sale.order.list'
    _description = 'Plan Sale Order List'

    approver = fields.Many2one('res.partner', string='Approver')
    approval_status = fields.Selection([
        ('unavailable', 'Unavailable'),
        ('approve', 'Approve'),
        ('refuse', 'Refuse'),
    ], string='Approval Status', default='unavailable', readonly=True)

    order_id = fields.Many2one('plan.sale.order', string='Order Reference')
    state_related = fields.Selection(related='order_id.state', string='State related')

    # Button approve for approver
    def btn_approve(self):
        self.approval_status = 'approve'
        temp = self.order_id.order_line.mapped('approval_status')
        if all([state == 'approve' for state in temp]):
            self.order_id.can_confirm = 'yes'

    # Button refuse for approver
    def btn_refuse(self):
        self.approval_status = 'refuse'
        temp = self.order_id.order_line.mapped('approval_status')
        if all([state == 'refuse' for state in temp]):
            self.order_id.can_confirm = 'no'
