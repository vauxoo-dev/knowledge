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
from openerp import models, fields, api, SUPERUSER_ID, _
from openerp.exceptions import Warning as UserError


class DocumentPageHistory(models.Model):
    """This class is use to manage Document History."""
    _inherit = 'document.page.history'

    approver_item_ids = fields.One2many(
        'approver.document.page.item', 'history_id', 'Approver items',
        help='Users and state in items that need partial approbation in '
        'this history')

    to_approve_ok = fields.Boolean(compute='_get_approver_ok')

    @api.depends('approver_item_ids.approved')
    def _get_approver_ok(self):
        """Return True if all Approver Items are approved."""
        for history in self:
            if all([item.approved for item in history.approver_item_ids]):
                history.to_approve_ok = True

    @api.multi
    def update_approver_items(self):
        """Refresh items by user based in page_id"""
        for history in self:
            users_approver = history.approver_item_ids.filtered(
                "approved").mapped('user_id')
            users_page = history.page_id.approver_item_ids.mapped('user_id')
            history.approver_item_ids.unlink()
            for user in users_page:
                self.env['approver.document.page.item'].create({
                    'history_id': history.id,
                    'user_id': user.id,
                    'approved': user.id in users_approver.ids})
        return True

    def page_approval_draft(self):
        """Overwrite method to change template to send mail"""
        self.write({'state': 'draft'})
        template_id = self.env['ir.model.data'].get_object_reference(
            'document_page_approval_levels',
            'email_template_new_history_need_approval')[1]
        for page in self:
            if page.is_parent_approval_required:
                self.env['email.template'].browse(template_id).send_mail(
                    page.id, force_send=True)
                msg = _('<div>New document to approve.</div>')
                page.page_id.message_post(
                    type='comment', body=msg)
        return True

    @api.multi
    def get_followers(self):
        follower_obj = self.env['mail.followers']
        fol_ids = follower_obj.sudo(SUPERUSER_ID).search([
            ('res_model', '=', 'document.page'),
            ('res_id', '=', self.page_id.id)])
        partner_ids = [
            foll.partner_id.email for foll in fol_ids if foll.partner_id]
        return ', '.join(map(str, partner_ids))

    @api.multi
    def write(self, values):
        """Inherit to notify that content in history is changed."""
        if 'content' in values:
            self._history_content_updated()
        return super(DocumentPageHistory, self).write(values)

    @api.multi
    def _history_content_updated(self):
        """When is changed the content in document page history:
            - Verify that the user is approver of the history
            - Disapprove items approved in the history
            - Send notification that the history was changed."""
        if self._uid not in self.approver_item_ids.mapped('user_id').ids:
            raise UserError(_('Invalid Action!'), _(
                'Only users validators can edit the content in this history.'))
        self.mapped('approver_item_ids').write({'approved': False})
        self.page_approval_draft()

    @api.multi
    def page_approval_approved(self):
        for history in self:
            history.page_id.with_context(from_history=True).write(
                {'content': history.content})
        self.page_approval_draft()
        return super(DocumentPageHistory, self).page_approval_approved()
