from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date
import xlsxwriter
from io import BytesIO
import base64

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
    
    def export_to_excel(self):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        sheet = workbook.add_worksheet("Purchase Request Details")

        # Định dạng
        bold = workbook.add_format({'bold': True, 'align': 'center', 'border': 1})
        currency_format = workbook.add_format({
            'num_format': '#,##0',
            'align': 'right',
            'border': 1
        })
        number_format = workbook.add_format({'align': 'right', 'border': 1})
        total_format = workbook.add_format({
            'bold': True,
            'align': 'right',
            'border': 1
        })

        # Thiết lập độ rộng cột
        sheet.set_column('A:A', 5)   # STT
        sheet.set_column('B:B', 15)  # Mã SP
        sheet.set_column('C:C', 40)  # Tên SP
        sheet.set_column('D:D', 10)  # Số lượng
        sheet.set_column('E:E', 15)  # Đơn vị
        sheet.set_column('F:G', 15)  # Giá và Thành tiền

        # Tiêu đề cột
        headers = ['STT', 'Mã Sản Phẩm', 'Tên Sản Phẩm', 'Số Lượng',
                  'Đơn Vị Tính', 'Giá Đơn Vị', 'Thành Tiền']
        for col_num, header in enumerate(headers):
            sheet.write(0, col_num, header, bold)

        # Ghi dữ liệu
        row = 1
        try:
            for index, line in enumerate(self.request_line_id, start=1):
                sheet.write(row, 0, index, number_format)
                sheet.write(row, 1, line.product_id.default_code or '', number_format)
                sheet.write(row, 2, line.product_id.name)
                sheet.write(row, 3, line.qty, number_format)
                sheet.write(row, 4, line.uom_id.name)
                sheet.write(row, 5, line.price_unit, currency_format)
                sheet.write(row, 6, line.qty * line.price_unit, currency_format)
                row += 1

            # Tổng cộng
            sheet.write(row, 2, "Tổng Cộng", total_format)
            sheet.write(row, 3, sum(line.qty for line in self.request_line_id),
                       total_format)
            sheet.write(row, 6, sum(line.qty * line.price_unit
                       for line in self.request_line_id), currency_format)

        except Exception as e:
            # Log lỗi nếu cần
            raise e

        workbook.close()
        excel_data = base64.b64encode(output.getvalue())

        attachment_vals = {
            'name': f'Purchase_Request_{self.name}.xlsx',
            'datas': excel_data,
            'store_fname': f'Purchase_Request_{self.name}.xlsx',
            'type': 'binary',
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        }

        attachment = self.env['ir.attachment'].create(attachment_vals)

        # Trả về URL download
        download_url = f'/web/content/ir.attachment/{attachment.id}/datas/{attachment.name}?download=true'

        return {
            'type': 'ir.actions.act_url',
            'url': download_url,
            'target': 'new',
        }


