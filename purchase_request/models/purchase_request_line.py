from odoo import models, fields, api

class PurchaseRequestLine(models.Model):
    _name = 'purchase.request.line'
    _description = 'Purchase Request Line'

    request_id = fields.Many2one(
        'purchase.request',
        string='Purchase Request',
        required=True,
        ondelete='cascade'
    )
    product_id = fields.Many2one(
        'product.template',
        string='Product',
        required=True
    )
    uom_id = fields.Many2one(
        'uom.uom',
        string='Unit of Measure',
        required=True
    )
    qty = fields.Float(
        string='Requested Quantity',
        required=True,
        default=1.0
    )
    qty_approve = fields.Float(
        string='Approved Quantity',
        readonly=True
    )
    price_unit = fields.Float(
        string='Unit Price',
        compute='_compute_price_unit',
        store=True
    ) #đưn giá
    total = fields.Float(
        string='Total',
        compute='_compute_total',
        store=True
    )

    @api.depends('product_id')
    def _compute_price_unit(self):
        for line in self:
            if line.product_id:
                line.price_unit = line.product_id.list_price  # Lấy giá từ sản phẩm

    @api.depends('qty', 'price_unit')
    def _compute_total(self):
        for line in self:
            line.total = line.qty * line.price_unit

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id.id
            self.price_unit = self.product_id.list_price
