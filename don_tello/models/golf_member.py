from odoo import models, fields, api

class GolfMember(models.Model):
    _name = 'golf.member'
    _description = 'Miembros del Club de Golf'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nombre completo', required=True, tracking=True)
    dni = fields.Char(string='DNI', required=True, tracking=True)
    edad = fields.Integer(string="Edad", required=True, tracking=True)
    jugador_golf = fields.Boolean(string='Jugador de Golf', default=True)
    email = fields.Char(string='Correo electrónico', tracking=True)
    phone = fields.Char(string='Teléfono')
    is_active = fields.Boolean(string='Activo', default=True)
    fecha_alta = fields.Date(string='Fecha de Alta', default=fields.Date.today)
    fecha_baja = fields.Date(string='Fecha de Baja')

    tipo_membresia_id = fields.Many2one(
        'golf.membership.type',
        string='Tipo de Membresía',
        default=lambda self: self.env.ref('don_tello.membership_type_club').id,
        required=True
    )

    cuota_mensual = fields.Float(
        string="Cuota mensual (€)",
        compute="_compute_cuota_mensual",
        store=True,
        readonly=True
    )

    partner_id = fields.Many2one('res.partner', string='Contacto Relacionado')

    cuotas_pendientes = fields.Integer(string='Cuotas Pendientes')
    currency_id = fields.Many2one('res.currency', string='Moneda', default=lambda self: self.env.company.currency_id.id)

    estado_pago = fields.Selection([
        ('al_dia', 'Al día'),
        ('pendiente', 'Pendiente'),
        ('moroso', 'Moroso'),
    ], string='Estado del Pago', default='al_dia', tracking=True,
       compute='_compute_estado_pago', store=True)

    # reservation_ids = fields.One2many('golf.reservation', 'member_id', string='Reservas')
    event_ids = fields.Many2many('golf.event', string='Eventos Participados')

    @api.depends('cuotas_pendientes')
    def _compute_estado_pago(self):
        for rec in self:
            if rec.cuotas_pendientes > 1:
                rec.estado_pago = 'moroso'
            elif rec.cuotas_pendientes == 1:
                rec.estado_pago = 'pendiente'
            else:
                rec.estado_pago = 'al_dia'

    @api.depends('tipo_membresia_id')
    def _compute_cuota_mensual(self):
        for rec in self:
            cuota_base = rec.tipo_membresia_id.monthly_fee or 0.0
            cuota_dj = 0.0

            if rec.tipo_membresia_id.code in ['BIRDIE', 'HOI']:
                # Buscar tarifa de derechos de juego para este plan
                plan = 'plan_birdie' if rec.tipo_membresia_id.code == 'BIRDIE' else 'hole_in_one'

                dj_tarifa = self.env['golf.fee.rate'].search([
                    ('type', '=', 'game_rights'),
                    ('user_type', '=', 'abonado'),
                    ('condition', '=', 'primer_jugador'),
                    ('active', '=', True),
                    ('name', 'ilike', plan.replace('_', ' '))
                ], limit=1)

                cuota_dj = dj_tarifa.price if dj_tarifa else 0.0

            rec.cuota_mensual = cuota_base + cuota_dj
