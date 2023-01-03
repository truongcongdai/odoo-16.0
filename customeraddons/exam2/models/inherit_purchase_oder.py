from odoo import models,fields
from odoo.exceptions import ValidationError
class InheritPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    department = fields.Many2one('hr.department', required=True, string='Department')
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
                            raise ValidationError("Đã vượt quá giới hạn xin vui lòng tạo activity cho người dùng thuộc nhóm kế toán vào xác nhận")
        else:
            raise ValidationError("Tài khoản không có giới hạn mua hàng")