# coding: utf-8
############################################################################
#    Module Writen For Odoo, Open Source Management Solution
#
#    Copyright (c) 2016 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
#    coded by: Luis Torres <luis_t@vauxoo.com>
#    planned by: Sabrina Romero <sabrina@vauxoo.com>
############################################################################
{
    "name": "Document Page Report",
    "version": "8.0.0.0.1",
    "author": "Vauxoo",
    "website": "https://www.vauxoo.com",
    "license": "AGPL-3",
    "category": "Knowledge Management",
    "depends": [
        "report",
        "document_page_approval_levels",
    ],
    "data": [
        "data/report_paperformat.xml",
        "view/layout.xml",
        "view/document_page_report.xml",
    ],
    "demo": [],
    "installable": True,
}
