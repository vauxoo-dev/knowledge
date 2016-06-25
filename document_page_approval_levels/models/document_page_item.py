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
from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError, ValidationError


class ApproverDocumentPageItem(models.Model):
    _name = 'approver.document.page.item'

    user_id = fields.Many2one(
        'res.users', 'User', required=True, help='User of committee that need '
        'approve partially the histories generated from this page.')

    approved = fields.Boolean(
        help='Indicate if this item already was approved')

    document_id = fields.Many2one('document.page', 'Document')

    history_id = fields.Many2one('document.page.history', 'History')

    @api.multi
    def approve(self):
        """Approve a document page and send an note in the register."""
        for item in self:
            if item.approved:
                continue
            if item._uid != item.user_id.id:
                raise UserError(
                    _('Invalid Action!'),
                    _('Only the user assigned to this item can validate it.'))
            item.write({'approved': True})
            msg = (
                '<div><b>The page has been approved by %s .</b></div>' %
                item.user_id.name)
            item.history_id.page_id.message_post(
                type='comment', body=_(msg))

    @api.constrains('user_id', 'document_id')
    def _check_unique_user_document(self):
        if all([self.user_id, self.document_id, self.search([
                ('user_id', '=', self.user_id.id),
                ('document_id', '=', self.document_id.id),
                ('id', '!=', self.id)])]):
            raise ValidationError(_(
                'Only can assign an item by the same user by document.'))

    @api.model
    def create(self, vals):
        res = super(ApproverDocumentPageItem, self).create(vals)
        res.document_id.message_subscribe_users(res.user_id.id)
        return res
