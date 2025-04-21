from odoo import models, fields

class GolfSport(models.Model):
    _name = 'golf.sport'
    _description = 'Escuela o Actividad Deportiva del Club'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True)
    code = fields.Char(string='Código', help="Código interno único de la actividad", required=True)
    description = fields.Text(string='Descripción')
    active = fields.Boolean(default=True, string='Activo')
    type = fields.Selection([
        ('infantil', 'Infantil'),
        ('adulto', 'Adulto'),
        ('mixto', 'Mixto')
    ], string='Categoría', default='mixto')

    default_price = fields.Float(string='Precio Base (si aplica)', help="Precio general de referencia")
    is_external = fields.Boolean(string='Gestionado Externamente', help="Marcar si la actividad no la gestiona directamente el club")
