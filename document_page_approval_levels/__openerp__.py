# coding: utf-8
############################################################################
#    Module Writen For Odoo, Open Source Management Solution
#
#    Copyright (c) 2016 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
#    coded by: Luis Torres <luis_t@vauxoo.com>
#    planned by: Sabrina Romero<sabrina@vauxoo.com>
############################################################################
{
    "name": "Document page approval levels",
    "version": "8.0.0.0.1",
    "author": "Vauxoo",
    "category": "Knowledge Management",
    "website": "http://www.vauxoo.com/",
    "license": "AGPL-3",
    "depends": [
        "base_action_rule",
        "document_page_approval",
    ],
    "demo": [
        "demo/res_users.xml",
    ],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "data/action_server_data.xml",
        "data/notification_template.xml",
        "views/document_page_item_view.xml",
        "views/document_page_view.xml",
        "views/document_page_history_view.xml",
    ],
    "test": [],
    "js": [],
    "css": [],
    "qweb": [],
    "installable": True,
    "auto_install": False
}
