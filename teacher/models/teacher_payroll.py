from odoo import models, fields, api

class TeacherPayroll(models.Model):
    _name = 'teacher.payroll'
    _description = 'Teacher Payroll'

    teacher_id = fields.Many2one('teacher.profile', string='Teacher', required=True)
    total_hours = fields.Float(string='Total Hours', compute='_compute_total_hours', inverse='_inverse_total_hours', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    total_salary = fields.Monetary(string='Total Salary', compute='_compute_total_salary', inverse='_inverse_total_salary', store=True)

    @api.depends('teacher_id')
    def _compute_total_hours(self):
        for record in self:
            attendances = self.env['teacher.attendance'].search([('teacher_id', '=', record.teacher_id.id)])
            record.total_hours = sum(attendance.hours_worked for attendance in attendances)

    def _inverse_total_hours(self):
        # Inverse method to adjust related attendance records based on total_hours changes
        for record in self:
            # Cập nhật trường hợp cần cập nhật `hours_worked` trong các bản ghi attendance
            attendances = self.env['teacher.attendance'].search([('teacher_id', '=', record.teacher_id.id)])
            hours_per_attendance = record.total_hours / len(attendances) if attendances else 0
            for attendance in attendances:
                attendance.hours_worked = hours_per_attendance

    @api.depends('total_hours', 'teacher_id')
    def _compute_total_salary(self):
        for record in self:
            record.total_salary = record.total_hours * record.teacher_id.salary_per_hour

    def _inverse_total_salary(self):
        for record in self:
            # Chỉ thực hiện thay đổi khi có `total_hours` và `salary_per_hour` hợp lệ
            if record.teacher_id.salary_per_hour:
                record.total_hours = record.total_salary / record.teacher_id.salary_per_hour
