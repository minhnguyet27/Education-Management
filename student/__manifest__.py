{
   'name': "Student Management",
   'summary': "Module for managing students and parents in the education system.",
   'description': """
   Student Management
   ==================
   This module provides functionalities to manage students, their profiles, and attendance records.
   
   Key Features:
   -------------
   * Student profile management
   * Parent information management
   * Attendance tracking
   """,
   'author': "Nguyet",
   'website': "https://izisolution.vn/",
   'category': 'Education',
   'version': '0.1.0',
   'depends': ['base','teacher'],
   'data': [
       'views/student_profile1.xml',
       'views/student_attendance.xml',
       'security/ir.model.access.csv',
       'security/group.xml',

   ],
#    'demo': ['demo/demo.xml'], 
   'installable': True,
   'application': True,
   'auto_install': True,
}
