from odoo import fields, models, api
from odoo.exceptions import UserError

class LeaveRequest(models.Model):
    _name = 'leave.request'
    _description = 'Leave Request'

    student_id = fields.Many2one('student.profile', string='Student', required=True)
    leave_date = fields.Date(string='Leave Date', required=True)
    reason = fields.Text(string='Reason', required=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='draft', string='Status',readonly=True)
    teacher_id = fields.Many2one('res.users', string='Teacher')
    approval_date = fields.Datetime(string='Approval Date')

    @api.model
    def create(self, vals):
        # Automatically assign the teacher as the current user (if not specified)
        if 'student_id' not in vals:
            vals['student_id'] = self.env.user.id
        if 'teacher_id' not in vals:
            vals['teacher_id'] = self.env.user.id  # Giáo viên có thể được gán tự động hoặc chọn thủ công
        return super(LeaveRequest, self).create(vals)

    def action_approve(self):
        # Only allow the teacher specified to approve the request
        if self.env.user != self.teacher_id:
            raise UserError("You can only approve leave requests assigned to you.")
        if self.status == 'approved':
            raise UserError("This request has already been approved.")
        self.status = 'approved'
        self.approval_date = fields.Datetime.now()

    def action_reject(self):
        # Only allow the teacher specified to reject the request
        if self.env.user != self.teacher_id:
            raise UserError("You can only reject leave requests assigned to you.")
        if self.status == 'rejected':
            raise UserError("This request has already been rejected.")
        self.status = 'rejected'
