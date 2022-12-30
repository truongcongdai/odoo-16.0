from odoo import models,fields
from odoo.exceptions import ValidationError
class InheritPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    department = fields.Many2one('hr.department', required=True, string='Department')
    check_send = fields.Boolean()
    #ghi de button_confirm
    def button_confirm(self):
        #lấy id của người dùng hiện
        current_user = self.env.uid
        # kiem tra tai khoan hien tai co thuoc nhom accountant
        check_group = self.user_has_groups('exam2.group_accountant_staff')
        #lay ra ban ghi co gioi han mua hang(limit purchase order) cao nhat
        purchase_limit_record = self.env['limit.purchase.order'].search([('name', '=', current_user)], order='order_limit DESC', limit=1)
        purchase_limit = purchase_limit_record.order_limit
        #nếu có giới hạn mua hàng thì...không thì sẽ raise lỗi
        if len(purchase_limit_record) > 0:
            for r in self:
                if r.amount_total:
                    if r.amount_total <= purchase_limit:
                        return super(InheritPurchaseOrder, self).button_confirm()
                    else:
                        if check_group:
                            return super(InheritPurchaseOrder, self).button_confirm()
                        else:
                            raise ValidationError("Đã vượt quá giới hạn")
        else:
            raise ValidationError("Tài khoản không có giới hạn mua hàng")

    def btn_send(self):
        mess_send = "Yêu cầu xác nhận được gửi vào %s" %(fields.Datetime.now())
        self.message_post(subject='Purchase Order New', body=mess_send)
        self.check_send = True



