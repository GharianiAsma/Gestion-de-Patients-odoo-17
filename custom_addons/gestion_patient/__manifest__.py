{
    'name': 'Gestion Hospitalière',
    'version': '1.0',
    'category': 'Healthcare',
    'summary': 'Système de gestion hospitalière',
    'description': """
        Module pour la gestion des patients, rendez-vous, employés, congés et factures dans un établissement hospitalier.
    """,
    'author': 'Data masters',
    'depends': ['base', 'mail', 'hr', 'hr_holidays', 'hr_skills'],
    'data': [
        'security/ir.model.access.csv',
        'security/security_rules.xml',
        'data/sequence_data.xml',
        'data/cron_jobs.xml',
        'views/patient_views.xml',
        'views/stats.xml',
        'views/gestion_rdv_views.xml',
        'views/hr_employee_views.xml',
        'views/hr_leave_views.xml',
        'views/liste_facture_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}

