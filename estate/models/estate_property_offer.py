from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float(required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_deadline",
        inverse="_inverse_deadline",
        store=True
    )
    property_id = fields.Many2one(
    "estate.property",
    required=True
    )

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)

    state = fields.Selection(
    selection=[("accepted", "Accepted"), ("refused", "Refused")],
    string="Status",
    copy=False,
    default=None
    )

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        if "accepted" in self.mapped("property_id.offer_ids.state"):
            raise UserError("An offer has already been accepted.")
        self.write({"state": "accepted"})
        return self.mapped("property_id").write({
            "state": "offer_accepted",
            "selling_price": self.price,
            "buyer_id": self.partner_id.id,
        })

    def action_refuse(self):
        return self.write({"state": "refused"})
    
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "The offer price must be strictly positive."),
    ]

