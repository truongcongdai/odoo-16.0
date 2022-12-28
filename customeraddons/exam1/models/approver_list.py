from odoo import models, fields

class ApproverList(models.Model):
    _name = 'approver.list'
    _inherit= ['mail.thread']

    approver = fields.Many2one('res.partner' , string='Approver')
    approver_status = fields.Selection(
        [('not approved yet', 'Not Approved Yet'),
         ('approve', 'Approve'),
         ('refuse', 'Refuse')], default='not approved yet', string='Approver Status')
    sale_order_id = fields.Many2one('plan.sale.order', string='Plan Sale Order')
    def btn_approve(self):
        mees_approve = "approval status approved on %s" %(fields.Datetime.now())
        self.approver_status = 'approve'
        states = self.sale_order_id.approve_id.mapped('approver_status')
        if all([state == 'approve'] for state in states):
            self.message_post(subject='Approve New Plan', body=mees_approve)
            self.sale_order_id.is_confirm = True

    def btn_refuse(self):
        mess_refuse = "approval status was denied on %s" % (fields.Datetime.now())
        self.approver_status = 'refuse'
        states = self.sale_order_id.approve_id.mapped('approver_status')
        if all([state == 'refuse'] for state in states):
            self.message_post(subject='Refuse New Plan', body=mess_refuse)
            self.sale_order_id.is_confirm =False