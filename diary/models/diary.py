from odoo import models, fields

class FormDiary(models.Model):
    _name = 'form.diary'
    _description = ''
    
    name = fields.Selection([
    ('quynay', 'Quý này'),
    ('dauquy', 'Đầu quý hiện tại'),
    ('nam', 'Năm nay'),
    ('daunam', 'Đến đầu năm nay'),
    ('t1', 'Tháng 1'),
    ('t2', 'Tháng 2'),
    ('t3', 'Tháng 3'),
    ('t4', 'Tháng 4'),
    ('t5', 'Tháng 5'),
    ('t6', 'Tháng 6'),
    ('t7', 'Tháng 7'),
    ('t8', 'Tháng 8'),
    ('t9', 'Tháng 9'),
    ('t10', 'Tháng 10'),
    ('t11', 'Tháng 11'),
    ('t12', 'Tháng 12'),
    ('q1', 'Quý 1'),
    ('q2', 'Quý 2'),
    ('q3', 'Quý 3'),
    ('q4', 'Quý 4'),
    ('tuantruoc', 'Tuần trước'),
    ('thangtruoc', 'Tháng trước'),
    ('quytruoc', 'Quý trước'),
    ('namtruoc', 'Năm trước'),
    ('4tuan', 'Bốn tuần sau'),
    ('thangsau', 'Tháng sau'),
    ('quysau', 'Quý sau'),
    ('namsau', 'Năm sau'),
    ('tuchon', 'Tự chọn'),
], string="Chọn kỳ báo cáo", default='nam')
    date_start = fields.Date(string='Từ', required=True, default=fields.Date.today)
    date_end = fields.Date(string='Đến', required=True, default=fields.Date.today)
    # source_id = fields.Many2one('account.source', string='Nguồn')
    source_id = fields.Char( string='Nguồn')
    program_id = fields.Char( string='Chương')
    # program_id = fields.Many2one('account.program', string='Chương')
    section_id = fields.Char( string='Khoản')
    # section_id = fields.Many2one('account.section', string='Khoản')
    filter_type = fields.Selection([
        ('all', 'Tất cả'),
        ('summary', 'Tổng hợp'),
        ('custom', 'Tùy chọn')
    ], string='Loại bộ lọc', default='all')
    combine_entries = fields.Boolean(string='Cộng gộp các bút toán giống nhau', default=False)
    template = fields.Selection([
        ('107', 'Thông tư 107/2017/TT-BTC'),
        ('other', 'Mẫu khác')
    ], string='Mẫu báo cáo', required=True, default='107')

    def action_save(self):
        self.ensure_one()
        # Thông báo thành công
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thành công',
                'message': 'Dữ liệu đã được lưu.',
                'type': 'success',
                'sticky': False,
            },
        }
