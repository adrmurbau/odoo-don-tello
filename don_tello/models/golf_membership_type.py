from odoo import models, fields

class GolfMembershipType(models.Model):
    _name = 'golf.membership.type'
    _description = 'Tipo de Membresía'

    name = fields.Char(string='Nombre', required=True)
    descripcion = fields.Text(string='Descripción')
    cuota_mensual = fields.Monetary(string='Cuota Mensual', currency_field='currency_id')
    currency_id = fields.Many2one(
        'res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id.id
    )
