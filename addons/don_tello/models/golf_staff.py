from odoo import models, fields

class GolfStaff(models.Model):
    _name = 'golf.staff'
    _description = 'Trabajador del Club de Golf'

    name = fields.Char(string='Nombre', required=True)
    department = fields.Selection([
        ('golf', 'Golf'),
        ('tennis', 'Pádel / Tenis'),
        ('equestrian', 'Equitación'),
        ('pool', 'Piscina')
    ], string='Departamento', required=True)
    phone = fields.Char(string='Teléfono')
    email = fields.Char(string='Correo Electrónico')
    active = fields.Boolean(default=True)
