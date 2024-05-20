from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Real estate property type module"
    _order = 'sequence, name'

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer(string="Sequence")
    offer_ids = fields.One2many("estate.property.offer", 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('property_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        ('name_is_unique', 'UNIQUE(name)', 'Name already exist')
    ]
