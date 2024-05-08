from datetime import date, timedelta

from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Real estate property offer module"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
    )
    partner_id = fields.Many2one('res.partner', string='Partner')
    property_id = fields.Many2one('estate.property', string='Property')
    validity = fields.Integer(compute='_compute_validity', inverse='_inverse_validity')
    date_deadline = fields.Date()

    @api.depends('date_deadline')
    def _compute_validity(self):
        for record in self:
            if not record.date_deadline:
                record.validity = None
            elif record.date_deadline:
                record.validity = (record.date_deadline.day - date.today().day)
            else:
                record.validity = -1

    def _inverse_validity(self):
        for record in self:
            self.date_deadline = record.create_date + timedelta(days=record.validity)
