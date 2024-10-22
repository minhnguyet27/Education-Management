from odoo import fields, models, api

class student_profile(models.Model):
   _name = 'student.profile'
   _description = 'Student Profile'

   student_code = fields.Char(string='Student Code', required=True)
   name = fields.Char(string='Student Name')
   birth = fields.Date(string='Birth Date')
   address = fields.Char(string='Address')
   gender = fields.Selection(string='Gender', selection=[('male', 'male'), ('female', 'female')])
   phone =  fields.Char(string='Phone Number')
   email =  fields.Char(string='Email')
   
   # One-to-many relation to attendance
   attendance_ids = fields.One2many('student.attendance', 'student_id', string="Attendance Records")
   # class_id = fields.Char(string='Class')
   # parent_id = fields.Char(string='Parent')
   is_editable = fields.Boolean(default=False)

   @api.multi
    def edit(self):
        # Logic to set the record in edit mode
        return True  # You might want to update the state or perform other actions

    @api.multi
    def save(self):
        # Logic to save the record
        self.write({
            'name': self.name,
            'description': self.description,
        })
        return True
  