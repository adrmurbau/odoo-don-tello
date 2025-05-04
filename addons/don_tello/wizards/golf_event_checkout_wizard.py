from odoo import models, fields, api
from odoo.exceptions import ValidationError

class GolfEventCheckoutWizard(models.TransientModel):
    _name = 'golf.event.checkout.wizard'
    _description = 'Asistente de Check-Out para Eventos'

    event_id = fields.Many2one('golf.event', string='Evento', required=True)
    member_id = fields.Many2one('golf.member', string='Miembro', required=True)

    @api.onchange('event_id')
    def _onchange_event_id(self):
        if self.event_id:
            checkin_no_salidos_ids = self.env['golf.event.attendance'].search([
                ('event_id', '=', self.event_id.id),
                ('checkout_time', '=', False),
            ]).mapped('member_id').ids

            return {
                'domain': {
                    'member_id': [('id', 'in', checkin_no_salidos_ids)]
                }
            }

    def action_checkout(self):
        asistencia = self.env['golf.event.attendance'].search([
            ('event_id', '=', self.event_id.id),
            ('member_id', '=', self.member_id.id),
            ('checkout_time', '=', False),
        ], limit=1)

        if not asistencia:
            raise ValidationError("Este miembro no ha hecho check-in o ya ha salido.")

        asistencia.checkout_time = fields.Datetime.now()
