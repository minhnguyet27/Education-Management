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
   'depends': ['base'],
   'data': [ 
      'views/teacher_profile.xml',
      'views/teacher_attendance.xml',

   ],
#    'demo': ['demo/demo.xml'], 
   'installable': True,
   'application': True,
   'auto_install': False,
}
