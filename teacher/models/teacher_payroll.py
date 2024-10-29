from odoo import models, fields, api

class TeacherPayroll(models.Model):
    _name = 'teacher.payroll'
    _description = 'Teacher Payroll'

    teacher_id = fields.Many2one('teacher.profile', string='Teacher', required=True)
    total_hours = fields.Float(string='Total Hours', compute='_compute_total_hours')
    total_salary = fields.Float(string='Total Salary', compute='_compute_total_salary')

    @api.depends('teacher_id')
    def _compute_total_hours(self):
        for record in self:
            attendances = self.env['teacher.attendance'].search([('teacher_id', '=', record.teacher_id.id)])
            record.total_hours = sum(attendance.hours_worked for attendance in attendances)

    @api.depends('total_hours', 'teacher_id')
    def _compute_total_salary(self):
        for record in self:
            record.total_salary = record.total_hours * record.teacher_id.salary_per_hour
