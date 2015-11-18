# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Document Page',
    'version': '9.0.1.0.0',
    'category': 'Knowledge Management',
    'author': 'OpenERP SA, Odoo Community Association (OCA)',
    'website': 'http://www.openerp.com/',
    'license': 'AGPL-3',
    'depends': [
        'knowledge',
    ],
    'data': [
        'wizard/document_page_create_menu.xml',
        'wizard/document_page_show_diff.xml',
        'views/document_page.xml',
        'security/document_page_security.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'demo/document_page.xml'
    ],
    'test': [
        'test/document_page_test00.yml'
    ],
    'installable': True,
    'auto_install': False,
    'css': ['static/src/css/document_page.css'],
}
