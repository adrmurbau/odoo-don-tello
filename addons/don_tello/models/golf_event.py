from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime
from datetime import timedelta

class GolfEvent(models.Model):
    _name = 'golf.event'
    _description = 'Evento o Torneo del Club de Golf'
    _order = 'date desc, name'

    name = fields.Char(string='Nombre', required=True)
    date = fields.Datetime(string='Fecha y hora', required=True)
    duration_hours = fields.Float(string='Duración (horas)', default=4.0)
    end_datetime = fields.Datetime(string='Fin del evento', compute='_compute_end_datetime', store=True)
    max_participants = fields.Integer(string="Máximo de Participantes", default=50)
    registration_deadline = fields.Date(string="Fecha límite de inscripción")

    location = fields.Char(string='Ubicación', default='Club de Golf Don Tello')
    type = fields.Selection([
        ('torneo', 'Torneo'),
        ('evento_social', 'Evento Social'),
        ('clinic', 'Clínic'),
        ('otro', 'Otro'),
    ], string='Tipo de Evento', required=True, default='torneo')

    description = fields.Text(string='Descripción')
    notes = fields.Text(string='Notas internas')

    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('confirmado', 'Confirmado'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ], string='Estado', default='borrador', tracking=True)

    responsible_id = fields.Many2one('res.users', string='Responsable', default=lambda self: self.env.user)

    member_ids = fields.Many2many('golf.member', string='Participantes')
    checkin_ids = fields.One2many('golf.event.attendance', 'event_id', string='Asistencias')

    # Cómputo del fin del evento
    @api.depends('date', 'duration_hours')
    def _compute_end_datetime(self):
        for record in self:
            if record.date:
                record.end_datetime = record.date + timedelta(hours=record.duration_hours)

    @api.constrains('member_ids', 'max_participants')
    def _check_max_participants(self):
        for event in self:
            if event.max_participants and len(event.member_ids) > event.max_participants:
                raise ValidationError("No se pueden registrar más participantes de los permitidos.")

    @api.constrains('member_ids')
    def _check_registration_deadline(self):
        today = fields.Date.today()
        for event in self:
            if event.registration_deadline and today > event.registration_deadline:
                raise ValidationError("No se pueden registrar participantes fuera del plazo de inscripción.")


    def action_checkin(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'golf.event.checkin.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_event_id': self.id},
        }

    def action_checkout(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'golf.event.checkout.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_event_id': self.id},
        }
    
    # def action_show_event_statistics(self):
    #     stats = self.env['golf.event'].read_group(
    #         domain=[('date', '>=', fields.Date.today().replace(month=1, day=1))],
    #         fields=['type'],
    #         groupby=['type']
    #     )

    #     message = "\n".join(
    #         f"- {rec['type'] or 'Sin tipo definido'}: {rec['type_count']} evento(s)"
    #         for rec in stats
    #     )

    #     return {
    #         'type': 'ir.actions.client',
    #         'tag': 'display_notification',
    #         'params': {
    #             'title': 'Estadísticas de Eventos',
    #             'message': message,
    #             'type': 'info',
    #             'sticky': False,
    #         }
    #     }



