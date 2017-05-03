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
from openerp.exceptions\
    import Warning as UserError, ValidationError


class TestDocumentApprovalLevelState(TransactionCase):

    def setUp(self):
        super(TestDocumentApprovalLevelState, self).setUp()
        self.page_obj = self.env['document.page']
        self.history_obj = self.env['document.page.history']
        self.item_obj = self.env['approver.document.page.item']
        self.follower_obj = self.env['mail.followers']

        self.category = self.env.ref('document_page.demo_category1')
        self.approver_group = self.env.ref('base.group_document_approver_user')
        self.document_user = self.env.ref(
            'document_page_approval_levels.document_page_user')
        self.document_approver = self.env.ref(
            'document_page_approval_levels.document_page_approver')
        self.document_manager = self.env.ref(
            'document_page_approval_levels.document_page_manager')

        self.category.write({
            'approval_required': True,
            'approver_gid': self.approver_group.id
        })

    def test_10_verify_followers(self):
        """Create a new document with items and verify users as followers"""
        page_id = self.page_obj.create({
            'name': 'Page Demo',
            'parent_id': self.category.id,
            'content': 'First version in document',
            'approver_item_ids': [(0, 0, {
                'user_id': self.document_approver.id,
            }), (0, 0, {
                'user_id': self.document_manager.id,
            })]
        })
        fol_ids = self.follower_obj.search([
            ('res_model', '=', 'document.page'),
            ('res_id', '=', page_id.id)
        ])
        partners = [follow.partner_id.id for follow in fol_ids]
        self.assertTrue(
            self.document_approver.partner_id.id in partners,
            'User approver not in followers')
        self.assertTrue(
            self.document_manager.partner_id.id in partners,
            'User manager not in followers')

    def test_20_approve_item(self):
        """Create a new document with items and the user approve it"""
        page_id = self.page_obj.create({
            'name': 'Page Demo',
            'parent_id': self.category.id,
            'content': 'First version in document',
            'approver_item_ids': [(0, 0, {
                'user_id': self.document_approver.id,
            })]
        })
        histories = page_id.history_ids
        item = self.item_obj.search([
            ('history_id', 'in', histories.ids),
        ])
        with self.assertRaisesRegexp(
                UserError,
                'Only the user assigned to this item can validate it.'):
            item.sudo(self.document_manager.id).approve()
        item.sudo(self.document_approver.id).approve()
        self.assertTrue(item.approved, 'Item not approved')

    def test_30_create_new_item_in_document(self):
        """Create a new document with an items, after add a new and check that
        is updated in the history"""
        page = self.page_obj.create({
            'name': 'Page Demo',
            'parent_id': self.category.id,
            'content': 'First version in document',
            'approver_item_ids': [(0, 0, {
                'user_id': self.document_manager.id,
            })]
        })
        histories = page.history_ids
        items1 = self.item_obj.search([
            ('history_id', 'in', histories.ids),
        ])
        page.write({
            'approver_item_ids': [(0, 0, {
                'user_id': self.document_approver.id})]
        })
        items2 = self.item_obj.search([
            ('history_id', 'in', histories.ids),
        ])
        self.assertNotEquals(
            len(items1), len(items2),
            'Items in history are not updated')

    def test_40_new_item_document_with_item_approvea(self):
        """Verify that when is add a new item, approved items are not removed
        """
        page = self.page_obj.create({
            'name': 'Page Demo',
            'parent_id': self.category.id,
            'content': 'First version in document',
            'approver_item_ids': [(0, 0, {
                'user_id': self.document_approver.id,
            })]
        })
        histories = page.history_ids
        item = self.item_obj.search([
            ('history_id', 'in', histories.ids),
        ])
        item.sudo(self.document_approver.id).approve()
        page.write({
            'approver_item_ids': [(0, 0, {
                'user_id': self.document_manager.id})]
        })
        item = self.item_obj.search([
            ('history_id', 'in', histories.ids),
            ('approved', '=', True)
        ])
        self.assertTrue(item, 'Item approved not found')

    def test_50_approve_item(self):
        """Create two items to the same user"""
        with self.assertRaisesRegexp(
                ValidationError,
                'Only can assign an item by the same user by document.'):
            self.page_obj.create({
                'name': 'Page Demo',
                'parent_id': self.category.id,
                'content': 'First version in document',
                'approver_item_ids': [(0, 0, {
                    'user_id': self.document_approver.id,
                }), (0, 0, {
                    'user_id': self.document_approver.id,
                })]
            })

    def test_60_try_delete_page_user(self):
        """Try delete a page with limit user"""
        page = self.page_obj.sudo(self.document_user.id).create({
            'name': 'Page Demo',
            'parent_id': self.category.id,
            'content': 'First version in document',
            'approver_item_ids': [(0, 0, {
                'user_id': self.document_approver.id,
            })]})
        page.sudo(self.document_user.id).unlink()

    def test_70_changed_content_in_history(self):
        """Test that update content in history"""
        page = self.page_obj.create({
            'name': 'Page Demo to Update',
            'parent_id': self.category.id,
            'content': 'First version in docume',
            'approver_item_ids': [(0, 0, {
                'user_id': self.document_approver.id,
            }), (0, 0, {
                'user_id': self.document_manager.id,
            })]
        })
        histories = page.history_ids
        item = self.item_obj.search([
            ('history_id', 'in', histories.ids),
            ('user_id', '=', self.document_approver.id)
        ])
        item.sudo(self.document_approver.id).approve()
        histories.sudo(self.document_manager.id).write({
            'content': 'First version in document'
        })
        items = self.item_obj.search([
            ('history_id', 'in', histories.ids),
            ('approved', '=', True)
        ])
        self.assertFalse(items, 'The Items must be disapproved')
        for item in histories.approver_item_ids:
            item.sudo(item.user_id.id).approve()
        histories.signal_workflow('page_approval_approve')
        self.assertEquals(
            page.content, histories.content, 'Content not updated')
        self.assertEquals(
            len(page.history_ids), 1, 'Histories created mistakenly')
