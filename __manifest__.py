{
    'name': 'Hospitals Management System',
    'author': 'Mona Ali',
    'summary': 'Hospital Management System module for Odoo.',
    'description': 'Managing patients in hospitals.',
    'category': 'Healthcare',
    'version': '0.1',
    'depends': ['crm'],
    'data': [
        'views/hms_patient_views.xml',
        'views/hms_doctor_views.xml',
        'views/hms_department_views.xml'
    ],
    'installable': True, # can install
    'application': True, # application and module
}
