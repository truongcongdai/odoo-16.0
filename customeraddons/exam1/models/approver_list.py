from odoo import models, fields

class ApproverList(models.Model):
    _name = 'approver.list'

    approver = fields.Many2one('res.partner' , string='Approver')
    approver_status = fields.Selection(
        [('not approved yet', 'Not Approved Yet'),
         ('approve', 'Approve'),
         ('refuse', 'Refuse')], default='not approved yet', string='Approver Status')
    sale_order_id = fields.Many2one('plan.sale.order', string='Plan Sale Order')
    def btn_approve(self):
        self.approver_status = 'approve'
        states = self.sale_order_id.approve_id.mapped('approver_status')
        if all([state == 'approve' for state in states]):
            self.sale_order_id.is_confirm = True
    def btn_refuse(self):
        self.approver_status = 'refuse'
        states = self.sale_order_id.approve_id.mapped('approver_status')
        if ([state == 'refuse'] for state in states):
            self.sale_order_id.is_confirm =False