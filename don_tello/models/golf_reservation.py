from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class GolfReservation(models.Model):
    _name = 'golf.reservation'
    _description = 'Reserva de Instalaciones'

    name = fields.Char(string='Referencia', required=True, default='Nueva')
    member_id = fields.Many2one('golf.member', string='Socio', required=True)
    reservation_date = fields.Datetime(string='Fecha de Reserva', required=True)
    facility = fields.Selection([
        ('campo_golf', 'Campo de Golf'),
        ('pista_tenis', 'Pista de Tenis'),
        ('sala_eventos', 'Sala de Eventos'),
    ], string='Instalación', required=True)
    notes = fields.Text(string='Notas')

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nueva') == 'Nueva':
            vals['name'] = self.env['ir.sequence'].next_by_code('golf.reservation') or 'Nueva'
        return super().create(vals)
