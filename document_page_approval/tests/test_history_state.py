# coding: utf-8
############################################################################
#    Module Writen For Odoo, Open Source Management Solution
#
#    Copyright (c) 2016 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
#    Coded by: Luis Torres (luis_t@vauxoo.com)
############################################################################
from openerp.tests.common import TransactionCase


class TestDocumentHistoryState(TransactionCase):

    def setUp(self):
        super(TestDocumentHistoryState, self).setUp()
        self.page_obj = self.env['document.page']
        self.history_obj = self.env['document.page.history']

        self.category = self.env.ref('document_page.demo_category1')
        self.approver_group = self.env.ref('base.group_document_approver_user')

        self.category.write({
            'approval_required': True,
            'approver_gid': self.approver_group.id
        })

    def test_10_history_state_no_all_approved(self):
        """Create a new document, and not validate the history"""
        page_id = self.page_obj.create({
            'name': 'Page Demo',
            'parent_id': self.category.id,
            'content': 'First version in document',
        })
        self.assertEquals(
            page_id.history_state, 'blocked',
            'Error, history state must be No all approved, because histories '
            'related are not approved')

    def test_20_history_state_approve(self):
        """Create a new document, and not validate the history"""
        page_id = self.page_obj.create({
            'name': 'Page Demo to Approve',
            'parent_id': self.category.id,
            'content': 'First version in document',
        })
        history_ids = self.history_obj.search([
            ('page_id', '=', page_id.id)
        ])
        history_ids.signal_workflow('page_approval_approve')
        self.assertEquals(
            page_id.history_state, 'done',
            'Error, history state must be Approved, because histories '
            'related are approved')
