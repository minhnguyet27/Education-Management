from odoo import fields, models, api

class student_profile(models.Model):
    _name = 'student.profile'
    _description = 'Student Profile'

    student_code = fields.Char(string='Student Code', required=True)
    name = fields.Char(string='Student Name', required=True)
    birth = fields.Date(string='Birth Date', required=True)
    address = fields.Char(string='Address', required=True)
    gender = fields.Selection(string='Gender', selection=[('male', 'male'), ('female', 'female')], required=True)
    phone =  fields.Char(string='Phone Number', required=True)
    email =  fields.Char(string='Email', required=True)
    active = fields.Boolean(string='Active', default=True)
    is_active_icon = fields.Boolean(string='Is Active Icon', compute='_compute_is_active_icon')   
    attendance_ids = fields.One2many('student.attendance', 'student_id', string="Attendance Records")
    # teacher_id = fields.Many2one('teacher.profile', string="Class Teacher")  # Quan hệ đến giáo viên

    _sql_constraints = [('unique_student_code_email', 'unique(student_code, email)', 'The combination of student code and email must be unique!')]

   # class_id = fields.Char(string='Class')
   # parent_id = fields.Char(string='Parent')
#    is_editable = fields.Boolean(default=False)
#    is_active = fields.Boolean(default=True)

    # @api.model(self)
    # def _compute_is_active_icon(self):
    #     for record in self:
    #         record.is_active_icon = record.active
#    @api.multi
#     def edit(self):
#         # Logic to set the record in edit mode
#         return True  # You might want to update the state or perform other actions

#     @api.multi
#     def save(self):
#         # Logic to save the record
#         self.write({
#             'name': self.name,
#             'description': self.description,
#         })
#         return True
  