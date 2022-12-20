from odoo import models,fields
from odoo.exceptions import ValidationError
class InheritPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    department = fields.Many2one('hr.department', required=True, string='Department')
    check_send = fields.Boolean()
    #ghi de button_confirm
    def button_confirm(self):
        #lay ra ban ghi co nhom la accountant
        accountant_group_record = self.env['res.groups'].search([('name', '=', 'Accountant')])
        #kiem tra tai khoan hien tai co thuoc nhom accountant
        current_user = self.env.uid
        check_group = current_user in accountant_group_record.users.ids
        #lay ra ban ghi co gioi han mua hang cao nhat
        purchase_limit_record = self.env['limit.purchase.order'].search([('name', '=', current_user)], order='order_limit DESC', limit=1)
        purchase_limit = purchase_limit_record.mapped('order_limit')
        if len(purchase_limit_record) > 0:
            for r in self:
                if r.amount_total:
                    if r.amount_total <= purchase_limit[0]:
                        return super(InheritPurchaseOrder, self).button_confirm()
                    else:

                        if check_group:
                            return super(InheritPurchaseOrder, self).button_confirm()
                        else:
                            raise ValidationError("The limit has been exceeded")
        else:
            raise ValidationError("Account has no purchase limit")

    def btn_send(self):
        mess_send = "Confirmation request sent on %s" %(fields.Datetime.now())
        self.message_post(subject='Purchase Order New', body=mess_send)
        for r in self:
            r.check_send = True



