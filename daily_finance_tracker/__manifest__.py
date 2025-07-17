{
    "name" : "Daily Finance Tracker",
    "version" : "1.0",
    "summary" : "Track inflows and outflows of money on a daily basis with frontend and Excel import/export",
    "description" : "This module allows users to track their daily financial transactions, including income and expenses. It features a user-friendly frontend for data entry and supports backend operations such as importing Excel files for bulk data management and exporting pdf",
    "author" : "Michael Ndunwa",
    "category" : "Accounting",
    "depends" : ["base", "web", "portal", "auth_signup", "mail"],
    "data" : [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/finance_entry_views.xml",
        "views/import_wizard_view.xml",
        "views/finance_entry_templates.xml",
        "views/finance_entry_report.xml",
    ],
    "assets" : {
        "web.assets_frontend" : [
            "daily_finance_tracker/static/src/css/form.css",
            "daily_finance_tracker/static/src/js/form.js",
        ],
    },
    "installable" : True,
    "application" : True,
    "license" : "LGPL-3",
}