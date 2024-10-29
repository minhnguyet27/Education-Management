from odoo import models, fields

class TeacherAttendance(models.Model):
    _name = 'teacher.attendance'
    _description = 'Teacher Attendance'

    teacher_id = fields.Many2one('teacher.profile', string='Teacher', required=True)
    date = fields.Date(string='Date', required=True)
    hours_worked = fields.Float(string='Hours Worked', required=True)
