from odoo import api, fields, models
from datetime import date

class TuitionFee(models.Model):
    _name = 'tuition.fee'
    _description = 'Tuition Fee Management'

    # Liên kết với model học sinh
    student_id = fields.Many2one('student.profile', string="Student", required=True)
    student_name = fields.Char(related='student_id.name', string='Student Name', readonly=True)
    # Các trường thông tin về học phí
    amount = fields.Float(string="Tuition Amount", required=True)
    due_date = fields.Date(string="Due Date", required=True)
    payment_date = fields.Date(string="Payment Date")
    status = fields.Selection([
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('late', 'Late'),
    ], string="Status", default='unpaid')

    @api.onchange('payment_date', 'due_date')
    def _onchange_payment_status(self):
        """Kiểm tra trạng thái thanh toán và cập nhật nếu quá hạn"""
        if self.payment_date and self.due_date:
            if self.payment_date > self.due_date:
                self.status = 'late'
            elif self.payment_date <= self.due_date:
                self.status = 'paid'
            else:
                self.status = 'unpaid'
