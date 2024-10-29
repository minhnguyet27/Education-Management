from odoo import fields, models, api

class student_attendance(models.Model):
    _name = 'student.attendance'
    _description = 'Student Attendance'

    # Many2one với bảng student_profile
    student_id = fields.Many2one('student.profile', string='Student')
    date = fields.Datetime(string="Date", default=fields.Datetime.now)
    status = fields.Selection([
         ('present', 'Present'),
         ('absent', 'Absent'),
         ('late', 'Late')
     ], string="Attendance Status", default='present')
    note = fields.Text(string="notes")
    

