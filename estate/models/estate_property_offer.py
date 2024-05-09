from datetime import date, timedelta

from odoo import fields, models, api, exceptions


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Real estate property offer module"
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        readonly=True
    )
    partner_id = fields.Many2one('res.partner', string='Partner')
    property_id = fields.Many2one('estate.property', string='Property')
    validity = fields.Integer(compute='_compute_validity', inverse='_inverse_validity')
    date_deadline = fields.Date()
    property_type_id = fields.Many2one(related='property_id.property_type_id', string='Property Type', store=True)

    _sql_constraints = [
        ('price_gte_zero', 'CHECK(price >= 0)', 'Price should be greater than or equal to zero')
    ]

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

    def action_set_state(self):
        for record in self:
            has_accepted = record.env.context.get('accepted')
            if has_accepted:
                for offer in record.property_id.offer_ids:
                    if offer.status == 'accepted':
                        raise exceptions.UserError("Another offer already accepted, cancel it first")
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
                record.property_id.state = 'offer_accepted'
                record.status = 'accepted'
            else:
                record.status = 'refused'
                record.property_id.buyer_id = None
                record.property_id.selling_price = None

        return True
