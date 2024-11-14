from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import date

class student_profile(models.Model):
    _name = 'student.profile'
    _description = 'Student Profile'
    _rec_name = 'student_code'

    student_code = fields.Char(string='Student Code', copy=False, index=True, default=lambda self:('New'))
    name = fields.Char(string='Student Name', required=True)
    birth = fields.Date(string='Birth Date', required=True)
    address = fields.Char(string='Address', required=True)
    gender = fields.Selection(string='Gender', selection=[('male', 'male'), ('female', 'female')], required=True)
    phone =  fields.Char(string='Phone Number', required=True)
    email =  fields.Char(string='Email', required=True)
    active = fields.Boolean(string='Active', default=True)
    is_active_icon = fields.Boolean(string='Is Active Icon')   
    attendance_ids = fields.One2many('student.attendance', 'student_id', string="Attendance Records")
    teacher_id = fields.Many2one('teacher.profile', string="Teacher")  # Quan hệ đến giáo viên
    tuition_fee_ids = fields.One2many('tuition.fee', 'student_id', string="Tuition Fees")


    _sql_constraints = [('unique_student_email', 'unique(email)', 'The combination of email must be unique!')]

    @api.constrains('phone')
    def _check_phone(self):
        for record in self:
            if not record.phone.isdigit() or len(record.phone) < 9 or len(record.phone) > 11:
                raise ValidationError("Trường phone phải chứa chữ số và dài từ 9 đến 11 ký tự")
    
    @api.model
    def create(self, vals):
        # Generate a new student code
        if 'student_code' not in vals or not vals['student_code']:
            # Get the last student code from the database
            last_student = self.search([], order='id desc', limit=1)
            if last_student:
                # Assuming student_code is a numeric value, increment it
                last_code_number = int(last_student.student_code[2:]) #lấy code cũ, loại bỏ tiền số hs ở đầu
                new_code_number = last_code_number + 1
                new_student_code = f"HS{str(new_code_number).zfill(5)}"  # 5 chữ số
            else:
                new_student_code = "HS00001"  # Starting code if no records exist

            vals['student_code'] = new_student_code
        return super(student_profile, self).create(vals)

    def __str__(self):
        return f"{self.student_code} - {self.name}"
    
    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.student_code}] {record.name}"
            result.append((record.id, name))
        return result
            
   # class_id = fields.Char(string='Class')
   # parent_id = fields.Char(string='Parent')
#    is_editable = fields.Boolean(default=False)
#    is_active = fields.Boolean(default=True)

    # @api.depend('active')
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
  