# -*- coding: utf-8 -*-
from openerp.tests import common
# Import logger
import logging

# Get the logger
_logger = logging.getLogger(__name__)


class TestDocumentPageHistoryWorkflow(common.TransactionCase):
    """Test document page history workflow."""

    def test_can_user_approve_this_page(self):
        """Test if a user can approve this page."""
        group = self.env['res.groups'].search([
            ('name', '=', 'Document approver')
        ])
        category = self.env.ref('document_page.demo_category1')
        category.approval_required = True
        category.approver_uid = group

        page = self.env['document.page'].create({
            'name': 'Test Page10',
            'parent_id': category.id
        })

        # history = self.env['document.page.history']
        # history_ids = history.search(
        #    [
        #        ('page_id', '=', page.id)
        #    ],
        #    limit=1,
        #    order='create_date DESC'
        #)
        #history_ids.signal_workflow('page_approval_draft')
        #state = history_ids.state == 'draft'
        # state = history_ids[0].page_id == page.id
        self.assertTrue(page.is_approval_required(page))

    def test_get_approvers_guids(self):
        """Get approver guids."""
        category = self.env.ref('document_page.demo_category1')
        category.approval_required = True
        pages = self.env['document.page.history'].search([
            ('page_id', '=', category.id)
        ])
        page = pages[0]
        approvers_guid = page.get_approvers_guids()
        self.assertTrue(len(approvers_guid) > 0)

    def test_get_approvers_email(self):
        """Get approver email."""
        category = self.env.ref('document_page.demo_category1')
        category.approval_required = True
        pages = self.env['document.page.history'].search([
            ('page_id', '=', category.id)
        ])
        page = pages[0]
        _logger.info("Email: " + str(page.get_approvers_email))
        self.assertIsNotNone(page.get_approvers_email)

    def test_get_page_url(self):
        """Test if page url exist."""
        category = self.env.ref('document_page.demo_category1')
        category.approval_required = True
        pages = self.env['document.page.history'].search([
            ('page_id', '=', category.id)
        ])
        page = pages[0]
        _logger.info("Page: " + str(page.get_page_url))
        self.assertIsNotNone(page.get_page_url)
