from odoo import models, fields, api

class InheritPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    supplier = fields.Char(string="Supplier",compute='_compute_supplier',store=True)
    product_id = fields.Many2one('product.product', domain=[('purchase_oke','=',True)], string="Product", index='btree_not_null')

    @api.depends('product_id')
    def _compute_supplier(self):
        min_price_type_int = 0
        for r in self:
            if r.product_id:
                #lay ra ban ghi co supplier gia nho nhat
                record_min_price_supplier = self.env['product.supplierinfo'].search(
                    [('product_tmpl_id', '=', int(r.product_id.product_tmpl_id))], order='price asc', limit=1)
                min_price_type_list = record_min_price_supplier.mapped('price')

                #conver min_price_type_list to min_price_type_int
                for i in min_price_type_list:
                    min_price_type_int = i

                #lay ra ban ghi co product_tmpl_id=product_id.product_tmpl_id va gia nho nhat
                price_supplier_line = self.env['product.supplierinfo'].search(
                    [('product_tmpl_id', '=' ,int(r.product_id.product_tmpl_id)),('price','=',min_price_type_int)], order='price asc')
                price_supplier = price_supplier_line.mapped('partner_id.name')
                if len(price_supplier) > 1:
                    delivery_time = self.env['product.supplierinfo'].search(
                        [('product_tmpl_id' , '=' , int(r.product_id.product_tmpl_id)),('price','=',min_price_type_int)], order='delay asc' , limit=1)
                    shortest_delivery_time = delivery_time.mapped('partner_id.name')
                    r.supplier = ''.join(shortest_delivery_time)
                else:
                    r.supplier = ''.join(price_supplier)

