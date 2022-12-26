from odoo import models,fields,api
from odoo.exceptions import UserError

class PlanSaleOder(models.Model):
    _name = 'plan.sale.order'
    _inherit = ['mail.thread']
    name= fields.Char(required=True)
    quotation = fields.Many2one('sale.order',string="Quotation", readonly=True, required=True)
    content = fields.Text(string="Content" ,required= True)
    state = fields.Selection([('new', 'New'),('send', 'Send'),('approve', 'Approve'),('refuse', 'Refuse')])
    approve_id = fields.One2many('approver.list', 'sale_order_id' , string='Aprrover')
    is_confirm = fields.Boolean()
    check_send = fields.Boolean(compute='_compute_check_send')

    def btn_new(self):
        self.state = 'new'
        self.approve_id.approver_status = 'not approved yet'

    def btn_send(self):

        mess_send = 'the new plan has been sent to the person in charge by email on %s . Created by %s' \
        %(fields.Datetime.now(), self.create_uid.name)


        if self.state == 'new' or self.state == 'refuse':
            if self.approve_id.approver:
                self.state = 'send'
                self.message_post(subject='Send to approver', body=mess_send)
            else:
                raise UserError('This plan does not have any approvers')
        else:
            raise UserError('Cannot send this approver')
    def btn_confirm_approve(self):

        mess_approve = "The new plan of %s has been approved on %s" % (self.create_uid.name, fields.Datetime.now())

        if self.is_confirm:
            if self.approve_id.approver:
                self.state = 'approve'
                self.message_post(subject='Approve New Plan', body=mess_approve)
            else:
                raise UserError('Please write your approvers.')
        else:
            raise UserError('Cannot confirm this approve. Please check your data.')
    def btn_confirm_refuse(self):

        mess_refuse = "The new plan of %s has been refused on %s" % (self.create_uid.name, fields.Datetime.now())

        if not self.is_confirm:
            self.state ='refuse'
            self.approve_id.approver_status='not approved yet'
            self.message_post(subject='Refuse New Plan', body=mess_refuse)
        else:
            raise UserError('Cannot confirm this approve. Please check your data.')
    #chỉ người tạo mới có thể nhìn thấy nút send
    @api.depends('create_uid')
    def _compute_check_send(self):
        current_user_ui = self.env.uid
        self.check_send = False
        if current_user_ui != int(self.create_uid):
            self.check_send = True