# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    version_count = fields.Integer(default=0)

    def action_create_version(self):
        for record in self:
            pdf, _ = self.env['ir.actions.report'].sudo()._render_qweb_pdf('sale.action_report_saleorder', [record.id])

            record.message_post(
                attachments=[(f'{record.name}.pdf', pdf)]
            )

            name = record.name.split('-')[0]
            record.name = f'{name}-{record.version_count}'
            record.version_count = record.version_count + 1
