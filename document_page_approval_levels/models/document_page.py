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
from openerp import models, fields, api


class DocumentPage(models.Model):
    """This class is use to manage Document."""
    _inherit = 'document.page'

    approver_item_ids = fields.One2many(
        'approver.document.page.item', 'document_id', 'Approver items',
        help='Users that partially approve the histories of this page.')

    default_approver_ids = fields.Many2many('res.users',
                                            'res_users_rel',
                                            'document_page_id',
                                            'user_id',
                                            'Default Approvers')

    def create_history(self, page_id, content):
        if self._context.get('from_history', False):
            return False
        return super(DocumentPage, self).create_history(page_id, content)

    @api.onchange('parent_id')
    def do_set_default_approvers(self):
        values = []
        for record in self:
            if self.parent_id and self.parent_id.default_approver_ids \
               and self.parent_id.type == "category" and \
               self.parent_id.approval_required is True:
                [values.append((0, 0, {'user_id': user})) for
                 user in self.parent_id.default_approver_ids.ids]
                record.update({'approver_item_ids': values})
