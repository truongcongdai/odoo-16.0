from odoo import models,fields
from odoo.exceptions import ValidationError
class InheritPurchaseOder(models.Model):
    _inherit = 'purchase.order'

    department = fields.Many2one('hr.department', required=True, string='Department')

    def button_confirm(self):

        # mess_send = "Confirmation request sent on %s" % (fields.Datetime.now())

        current_user = self.env.uid
        employees = self.env['limit.purchase.order'].search([('name', '=', current_user)], order='order_limit DESC', limit=1)
        employee = employees.mapped('order_limit')
        for r in self:
            if r.amount_total:
                if r.amount_total <= employee[0]:
                    return super(InheritPurchaseOder, self).button_confirm()
                else:
                    print("oke")
                    # self.message_post(subject='Send New', body=mess_send)
                    raise ValidationError("The limit has been exceeded")


    def btn_send(self):
        mess_send = "Confirmation request sent on %s" %(fields.Datetime.now())
        self.message_post(subject='Purchase Order New', body=mess_send)

    def btn_confirm_order(self):
        return super(InheritPurchaseOder, self).button_confirm()