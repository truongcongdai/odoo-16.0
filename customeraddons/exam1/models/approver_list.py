from odoo import models, fields
from odoo.exceptions import UserError


class ApproverList(models.Model):
    _name = 'approver.list'

    def _selection_group(self):
        # lấy ra record của accountant
        groups_approve = self.env['res.groups'].search([('name', '=', 'Accountant')])
        # lấy ra id trong res_partner của nhóm acoountant
        res_users_id = groups_approve.users.mapped('partner_id').mapped('id')
        return [('id', 'in', res_users_id)]

    approver = fields.Many2one('res.partner', string='Approver', domain=_selection_group)
    approver_status = fields.Selection(
        [('not approved yet', 'Not Approved Yet'),
         ('approve', 'Approve'),
         ('refuse', 'Refuse')], default='not approved yet', string='Approver Status')
    check_approve = fields.Boolean(compute='_compute_check_approve')
    sale_order_id = fields.Many2one('plan.sale.order', string='Plan Sale Order')

    def btn_approve(self):
        mess_approve = "Kế hoạch mới của %s đã được phê duyệt vào %s" % (self.create_uid.name, fields.Datetime.now())
        if self.sale_order_id.state == 'send':
            self.approver_status = 'approve'
            states = self.sale_order_id.approve_id.mapped('approver_status')
            if all([state == 'approve' for state in states]):
                self.sale_order_id.state = 'approve'
                self.sale_order_id.message_post(subject='Phê duyệt kế hoạch mới', body=mess_approve)
        else:
            raise UserError('người dùng chưa gửi yêu cầu duyệt')

    def btn_refuse(self):
        mess_refuse = "Kế hoạch mới của %s đã bị từ chối vào %s" % (self.create_uid.name, fields.Datetime.now())
        if self.sale_order_id.state == 'send':
            self.approver_status = 'refuse'
            states = self.sale_order_id.approve_id.mapped('approver_status')
            if ([state == 'refuse'] for state in states):
                self.sale_order_id.state = 'refuse'
                self.sale_order_id.approve_id.approver_status = 'not approved yet'
                # print(self.env.user.partner_id.name)
                self.sale_order_id.message_post(subject='Từ chối kế hoạch mới', body=mess_refuse)
        else:
            raise UserError('người dùng chưa gửi yêu cầu duyệt')

    # chỉ được duyệt hoặc từ chối duyệt cho approver mà mình được phân công
    def _compute_check_approve(self):
        approvers = self.sale_order_id.approve_id.mapped('approver.name')
        for i in range(0, len(approvers)):
            # kiểm tra lần lượt approver trong database approver_list nếu trùng tên thì sẽ cho duyệt hoặc từ chối duyệt
            if approvers[i] == self.env.user.partner_id.name:
                self.sale_order_id.approve_id[i].check_approve = True
            else:
                self.sale_order_id.approve_id[i].check_approve = False
