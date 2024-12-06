{
    'name': 'Purchase Request',
    'version': '1.0',
    'summary': 'Mô tả ngắn gọn về module',
    'license': 'LGPL-3',
    'description': """
       Description
    """,
    'author': 'Nguyet',
    'website': 'https://website-cua-ban.com',
    'category': 'Purchases',
    'depends': ['base','hr','product','purchase'],
    'data': [ 
        'security/group_security.xml',
        'security/ir.model.access.csv',
        'security/ir.rule.xml',        
        'views/purchase_request.xml',
        'views/purchase_request_line.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
