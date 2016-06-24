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
from openerp import api, models


class DocumentPageReport(models.AbstractModel):
    _name = "report.document_page_report.page_report"

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env["report"]
        report = report_obj._get_report_from_name(
            "document_page_report.page_report")
        docargs = {
            "doc_ids": self._ids,
            "doc_model": report.model,
            "docs": self,
            "get_qty_reviews": self._get_qty_reviews,
        }
        return report_obj.render(
            "document_page_report.page_report", docargs)

    @api.multi
    def _get_qty_reviews(self, page):
        """Return qty of histories approved"""
        return len(page.history_ids.filtered(lambda r: r.state == 'approved'))
