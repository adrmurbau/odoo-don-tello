from odoo import models, fields, api
from odoo.exceptions import ValidationError

class GolfEventCheckinWizard(models.TransientModel):
    _name = 'golf.event.checkin.wizard'
    _description = 'Asistente de Check-In para Eventos'

    event_id = fields.Many2one('golf.event', string='Evento', required=True)
    member_id = fields.Many2one('golf.member', string='Miembro', required=True)


    @api.onchange('event_id')
    def _onchange_event_id(self):
        if self.event_id:
            asistentes_ids = self.env['golf.event.attendance'].search([
                ('event_id', '=', self.event_id.id)
            ]).mapped('member_id').ids

            disponibles_ids = self.event_id.member_ids.filtered(lambda m: m.id not in asistentes_ids).ids

            return {
                'domain': {
                    'member_id': [('id', 'in', disponibles_ids)]
                }
            }

    def action_checkin(self):
        # Comprobación extra por si acaso
        if self.member_id not in self.event_id.member_ids:
            raise ValidationError("Este miembro no está registrado como participante del evento.")

        self.env['golf.event.attendance'].create({
            'event_id': self.event_id.id,
            'member_id': self.member_id.id,
            'checkin_time': fields.Datetime.now(),
        })
