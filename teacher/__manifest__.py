{
   'name': "Teacher Management",
   'summary': "Module for managing teachers in the education system.",
   'description': """
   Teacher Management
   ==================
   This module provides functionalities to manage teachers, their profiles, and attendance records.
   
   Key Features:
   -------------
   * Teacher profile management
   * Parent information management
   * Attendance tracking
   """,
   'author': "Nguyet",
   'website': "https://izisolution.vn/",
   'category': 'Education',
   'version': '0.1.0',
   'depends': ['base','web'],
   'data': [    
      'views/teacher_payroll.xml',
      'report/report_teacher_payroll.xml',
      'views/teacher_attendance.xml',
      'views/teacher_profile.xml',
      'security/education_category.xml',
      'security/teacher_security.xml',
      'security/ir.model.access.csv',

   ],
#    'demo': ['demo/demo.xml'], 
   'installable': True,
   'application': True,
   'auto_install': False,
}
