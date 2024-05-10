from datetime import timedelta
from odoo import api, fields, models, exceptions
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Real estate property module"
    _order = 'property_type_id, id desc'

    name = fields.Char(string="Name", required=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=(fields.Datetime.today() + timedelta(days=90)), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('east', "East"), ('west', "West"), ('north', "North"), ('south', "South")],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        default='new',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'),
                   ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        readonly=True
    )
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False, )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", 'property_id', string="Offers")
    total_area = fields.Float(compute='_compute_total_area')
    best_offer = fields.Char(string="Best Offer", compute='_compute_best_offer')
    best_offer_price = fields.Integer(default=0)

    _sql_constraints = [
        ('expected_price_gte_zero', 'CHECK(expected_price >= 0)',
         'Expected Price should be greater than or equal to zero'),
        ('selling_price_gte_zero', 'CHECK(selling_price >= 0)', 'Selling Price should be greater than or equal to zero')
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        self.total_area = self.living_area + self.garden_area

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        best_offer = None
        for offer in self.offer_ids:
            if best_offer is None:
                best_offer = offer
            elif best_offer.price < offer.price:
                best_offer = offer

        if not best_offer:
            self.best_offer = 'No offer yet'
        else:
            self.best_offer = f'{best_offer.price}' + (f' by {best_offer.partner_id.name}' if best_offer.partner_id else '')
            self.best_offer_price = best_offer.price

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = ''

    def action_set_state(self):
        for record in self:
            if record.state == 'cancelled':
                raise exceptions.UserError('Property already cancelled')
            state = record.env.context.get('state')
            record.state = state
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, 3):
                return True
            acceptance_price = record.expected_price * (0.9)
            if float_compare(record.selling_price, acceptance_price, 0) == -1:
                raise exceptions.ValidationError('Selling price must be minimum 90% of acceptable price')

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise exceptions.UserError('Cannot delete property that are not in "New" or "Cancelled"')
