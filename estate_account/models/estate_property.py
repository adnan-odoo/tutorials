from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_state(self):
        super(EstateProperty, self).action_set_state()

        for record in self:
            invoice = {
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'line_ids': [
                    Command.create({
                        "name": record.name,
                        "quantity": 1,
                        "price_unit": record.selling_price * 0.06,
                    }),
                    Command.create({
                        "name": "Administrative fee",
                        "quantity": 1,
                        "price_unit": 100,
                    })
                ]
            }

            self.env['account.move'].create(invoice)

        return True
