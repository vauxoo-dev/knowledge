# coding: utf-8
############################################################################
#    Module Writen For Odoo, Open Source Management Solution
#
#    Copyright (c) 206 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
#    coded by: Luis Torres <luis_t@vauxoo.com>
#    planned by: Sabrina Romero <sabrina@vauxoo.com>
############################################################################
from openerp import models, fields


class DocumentPage(models.Model):
    """This class is use to manage Document."""
    _inherit = 'document.page'

    approver_item_ids = fields.One2many(
        'approver.document.page.item', 'document_id', 'Approver items',
        help='Users that partially approve the histories of this page.')

    def create_history(self, page_id, content):
        if self._context.get('from_history', False):
            return False
        return super(DocumentPage, self).create_history(page_id, content)
