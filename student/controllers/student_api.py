from odoo import http
from odoo.http import request

class StudentAPI(http.Controller): 
    @http.route('/api/students',auth='none', type='json', methods=['GET'])
    def get_students(self,**kwargs):
        """API Lấy danh sách thông tin học sinh"""
        try: 
            students = request.env['student.profile'].sudo().search([])
            result = []
            for student in students:
                result.append({
                    'id': student.id,
                    'student_code': student.student_code,
                    'name': student.name,
                    # 'gender': student.gender,
                    # 'email': student.email,
                    # 'address': student.address,
                    # 'phone': student.phone,
                    })
            return {'data': result}
        except Exception as e:
            return {'error': str(e)}, 500

        

