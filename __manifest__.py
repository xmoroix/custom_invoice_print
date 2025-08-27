{
    'name': 'Custom Invoice Print',
    'version': '16.0.1.1.0',  # Increment version for timbre integration
    'summary': 'Clinic and Client invoice printing with Algerian Timbre Tax',
    'description': 'Fixes Clinic Invoice to show product names and adds Client Invoice with category bundling. Enhanced with Algerian Timbre Tax integration for complete compliance.',
    'author': 'Bilal Benmerzoug',
    'depends': ['account', 'product', 'sale', 'l10n_dz_timbre_professional'],
    'data': [
        'security/ir.model.access.csv',
        'reports/clinic_invoice_report.xml',
        'reports/client_invoice_report.xml',
        'reports/clinic_quotation_report.xml',
        'reports/client_quotation_report.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'category': 'Accounting/Accounting',
    'license': 'LGPL-3',
}