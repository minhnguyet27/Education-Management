{
    'name': 'Diary',
    'version': '1.0',
    'summary': 'Mô tả ngắn gọn về module',
    'description': """
       Description
    """,
    'author': 'Nguyet',
    'website': 'https://website-cua-ban.com',
    'category': 'Custom',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',  
        'views/diary.xml',         
       
    ],
   #  'demo': [
   #      'data/demo_data.xml',           
   #  ],
    'installable': True,
    'application': True,
    'auto_install': True,
}
