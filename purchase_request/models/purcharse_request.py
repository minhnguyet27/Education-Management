from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date

class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Purchase Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Kế thừa để sử dụng chatter

    name = fields.Char(
        string='Request Reference',
        required=True,
        readonly=True,
        default='New',  # Tạm thời gán giá trị mặc định là 'New'
        copy=False,
    )   
    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        required=True,
        default=lambda self: self.env.user.department_id,  # Mặc định phòng ban của người dùng hiện tại
        
    ) #Liên kết đến phòng ban yêu cầu.
    request_id = fields.Many2one(
        'res.users',
        string='Requested By',
        default=lambda self: self.env.user,  # Mặc định là người dùng hiện tại       
    )
    company_id = fields.Many2one('res.company', string="Công ty", default=lambda self: self.env.user.company_id)
    approver_id = fields.Many2one(
        'res.users',
        string='Approver',default=lambda self: self.env.user,
        readonly=True
    ) #user xác nhận
    # picking_id = fields.Many2one('pick')
    date = fields.Date(
        string='Request Date',
        default=fields.Date.context_today,
        required=True, readonly=True
    )
    date_approve = fields.Date(
        string='Approval Date',
        readonly=True
    ) #ngày xác nhận
    request_line_ids = fields.One2many(
        'purchase.request.line','request_id', string='Request Lines'
    ) #chi tiết ds sản phẩm
    description = fields.Text(string='Mô tả')
    state = fields.Selection(
        [('draft', 'Dự thảo'),
         ('wait', 'Chờ duyệt'),
         ('approved', 'Được phê duyệt'),
         ('cancel', 'Đã từ chối'),
         ('done', 'Hoàn thành')],
        string='Status',
        default='draft',
        tracking=True
    )
    total_qty = fields.Float(
        string='Total Quantity',
        compute='_compute_totals',
        store=True
    )
    total_amount = fields.Float(
        string='Total Amount',
        compute='_compute_totals',
        store=True
    )
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            # Lấy giá trị lớn nhất hiện có để sinh mã mới
            last_record = self.search([], order="id desc", limit=1)
            next_number = 1
            if last_record and last_record.name.startswith('PR'):
                # Trích xuất số từ chuỗi name, ví dụ: PR00001 -> 1
                try:
                    next_number = int(last_record.name[2:]) + 1
                except ValueError:
                    next_number = 1
            # Tạo mã mới với định dạng PR+5 số
            vals['name'] = f"PR{str(next_number).zfill(5)}"
        return super(PurchaseRequest, self).create(vals)

    @api.depends('request_line_ids.qty', 'request_line_ids.total')
    def _compute_totals(self):
        for record in self:
            record.total_qty = sum(line.qty for line in record.request_line_ids) #tổng SL product
            record.total_amount = sum(line.total for line in record.request_line_ids) #Giá trị tổng

    def action_send_request(self):
        if not self.request_line_ids:
            raise UserError("Thêm ít nhất 1 sản phẩm")
        self.state = 'wait'
    #chỉ cho xóa trạng thái nháp
    def unlink(self):
        for record in self:
            if record.state != 'draft':
                raise UserError(("Chỉ được xóa khi ở trạng thái nháp"))
        return super(PurchaseRequest, self).unlink()
    #duyệt
    def action_approve(self):
        self.state = 'approved'
        self.date_approve = fields.Date.today()
    #hủy
    def action_cancel(self):
        self.state = 'cancel'
    #trở về nháp
    def action_reset_to_draft(self):
        self.state = 'draft'
    #lưu
    def action_save(self):
        self.ensure_one()


