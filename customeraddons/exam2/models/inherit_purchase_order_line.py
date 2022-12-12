from odoo import models, fields, api

class InheritPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    supplier = fields.Char(string="Supplier",compute='_compute_supplier',store=True)
    product_id = fields.Many2one('product.product', domain=[('purchase_oke','=',True)], string="Product", index='btree_not_null')

    @api.depends('product_id')
    def _compute_supplier(self):
        # for r in self:
        #     if r.product_id:
        #         list_record_supplier = self.env['product.supplierinfo'].search([('product_tmpl_id', '=' ,r.product_id.id)])
        #         record_min_price_supplier = self.env['product.supplierinfo'].search([('product_tmpl_id', '=' ,r.product_id.id)], order='price asc' , limit= 1)
        #         min_price = record_min_price_supplier.mapped('partner_id.name')
        #         print(min_price,record_min_price_supplier)

        for r in self:
            if r.product_id:
                record_min_price_supplier = self.env['product.supplierinfo'].search(
                    [('product_tmpl_id', '=', int(r.product_id.product_tmpl_id))], order='price asc', limit=1)
                min_price = record_min_price_supplier.mapped('price')

                price_supplier_line = self.env['product.supplierinfo'].search(
                    [('product_tmpl_id', '=' ,int(r.product_id.product_tmpl_id)),('price','=',min_price[0])], order='price asc')
                price_supplier = price_supplier_line.mapped('partner_id.name')
                if len(price_supplier) > 1:
                    delivery_time = self.env['product.supplierinfo'].search(
                        [('product_tmpl_id' , '=' , int(r.product_id.product_tmpl_id)),('price','=',min_price[0])], order='delay asc' , limit=1)
                    shortest_delivery_time = delivery_time.mapped('partner_id.name')
                    r.supplier = ''.join(shortest_delivery_time)
                else:
                    r.supplier = ''.join(price_supplier)

        # for r in self:
        #     if r.product_id:
        #         price_supplier_line = self.env['product.supplierinfo'].search(
        #             [('product_tmpl_id', '=' ,r.product_id.id)], order='price asc')
        #         price_supplier = price_supplier_line.mapped('partner_id.name')
        #         print(int(r.product_id.product_tmpl_id))
        #         if len(price_supplier) > 1:
        #             delivery_time = self.env['product.supplierinfo'].search(
        #                 [('product_tmpl_id' , '=' , r.product_id.id)], order='delay asc' , limit=1)
        #             shortest_delivery_time = delivery_time.mapped('partner_id.name')
        #             r.supplier = ''.join(shortest_delivery_time)
        #         else:
        #             r.supplier = ''.join(price_supplier)

