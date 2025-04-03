from odoo import models, fields

class GolfEvent(models.Model):
    _name = 'golf.event'
    _description = 'Evento del Club de Golf'

    name = fields.Char(string='Nombre del Evento', required=True)
    date = fields.Date(string='Fecha del Evento', required=True)
    location = fields.Char(string='Ubicación')
    description = fields.Text(string='Descripción')
    member_ids = fields.Many2many('golf.member', string='Participantes')
