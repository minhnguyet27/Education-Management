from odoo import models, fields

class TeacherProfile(models.Model):
    _name = 'teacher.profile'
    _description = 'Teacher Profile'

    name = fields.Char(string='Name', required=True)
    identification_id = fields.Char(string='Identification Number', required=True)
    hire_date = fields.Date(string='Hire Date')
    salary_per_hour = fields.Float(string='Salary per Hour', required=True)
