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
        mess_send = 'kế hoạch mới đã được gửi đến người phụ trách qua email vào ngày %s . Tạo bởi %s' %(fields.Datetime.now(), self.create_uid.name)
        if self.state == 'new' or self.state == 'refuse':
            if self.approve_id.approver:
                self.state = 'send'
                self.message_post(subject='Gửi tới người phê duyệt', body=mess_send)
            else:
                raise UserError('Kế hoạch này không có bất kỳ người phê duyệt')
        else:
            raise UserError('Không thể gửi người phê duyệt này')
    def btn_confirm_approve(self):
        mess_approve = "Kế hoạch mới của %s đã được phê duyệt vào %s" % (self.create_uid.name, fields.Datetime.now())
        if self.state == 'send':
            if self.is_confirm:
                if self.approve_id.approver:
                    self.state = 'approve'
                    self.message_post(subject='Approve New Plan', body=mess_approve)
                else:
                    raise UserError('Vui lòng viết người phê duyệt của bạn.')
            else:
                raise UserError('Không thể xác nhận phê duyệt này. Vui lòng kiểm tra dữ liệu của bạn.')
        else:
            raise UserError('người dùng chưa gửi yêu cầu')
    def btn_confirm_refuse(self):
        mess_refuse = "Kế hoạch mới của %s đã bị từ chối vào %s" % (self.create_uid.name, fields.Datetime.now())
        if self.state == 'send':
            if not self.is_confirm:
                self.state ='refuse'
                self.approve_id.approver_status='not approved yet'
                self.message_post(subject='Refuse New Plan', body=mess_refuse)
            else:
                raise UserError('Không thể xác nhận phê duyệt này. Vui lòng kiểm tra dữ liệu của bạn.')
        else:
            raise UserError('người dùng chưa gửi yêu cầu')
    #chỉ người tạo mới có thể nhìn thấy nút send
    @api.depends('create_uid')
    def _compute_check_send(self):
        current_user_ui = self.env.uid
        self.check_send = False
        if current_user_ui != int(self.create_uid):
            self.check_send = True