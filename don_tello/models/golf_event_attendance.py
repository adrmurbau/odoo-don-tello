from odoo import models, fields

class GolfEventAttendance(models.Model):
    _name = 'golf.event.attendance'
    _description = 'Asistencia a Eventos'

    event_id = fields.Many2one('golf.event', string='Evento', required=True, ondelete='cascade')
    member_id = fields.Many2one('golf.member', string='Miembro', required=True, ondelete='restrict')
    checkin_time = fields.Datetime(string='Hora de Entrada')
    checkout_time = fields.Datetime(string='Hora de Salida')
