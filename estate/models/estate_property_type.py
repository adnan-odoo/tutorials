from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Real estate property type module"

    name = fields.Char(string="Name", required=True)

    _sql_constraints = [
        ('name_is_unique', 'UNIQUE(name)', 'Name already exist')
    ]
