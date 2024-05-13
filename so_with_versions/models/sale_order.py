# -*- coding: utf-8 -*-

from odoo import models, fields, api


def _extract_name_and_version(name):
    if '-' in name:
        name, version = name.rsplit('-', 1)
        return name, int(version)
    return name, 0


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_create_version(self):
        for record in self:
            name, version = _extract_name_and_version(record.name)
            pdf, _ = self.env['ir.actions.report'].sudo()._render_qweb_pdf('sale.action_report_saleorder', [record.id])

            record.message_post(
                attachments=[
                    (f'{record.name}.pdf', pdf),
                ]
            )

            record.name = f'{name}-{version + 1}'
