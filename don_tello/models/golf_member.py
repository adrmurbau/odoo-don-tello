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

    tipo_membresia_id = fields.Many2one('golf.membership.type', string='Tipo de Membresía', tracking=True)
    tipo_membresia_auto = fields.Char(string='Membresía Asignada', compute='_compute_tipo_membresia', store=True, readonly=True)

    partner_id = fields.Many2one('res.partner', string='Contacto Relacionado')

    cuotas_pendientes = fields.Integer(string='Cuotas Pendientes')
    currency_id = fields.Many2one('res.currency', string='Moneda', default=lambda self: self.env.company.currency_id.id)

    estado_pago = fields.Selection([
        ('al_dia', 'Al día'),
        ('pendiente', 'Pendiente'),
        ('moroso', 'Moroso'),
    ], string='Estado del Pago', default='al_dia', tracking=True,
    compute='_compute_estado_pago', store=True)

    reservation_ids = fields.One2many('golf.reservation', 'member_id', string='Reservas')
    event_ids = fields.Many2many('golf.event', string='Eventos Participados')

    @api.depends('cuotas_pendientes')
    def _compute_estado_pago(self):
        for rec in self:
            if rec.cuotas_pendientes > 0 and rec.cuotas_pendientes <= 1:
                rec.estado_pago = 'pendiente'
            elif rec.cuotas_pendientes>1:
                rec.estado_pago='moroso'
            else:
                rec.estado_pago = 'al_dia'

    @api.depends('edad', 'jugador_golf')
    def _compute_tipo_membresia(self):
        for rec in self:
            tipo = "No clasificado"
            if not rec.jugador_golf:
                tipo = "No Jugador"
            elif rec.edad <= 0:
                tipo = "Desconocida"
            elif rec.edad < 15:
                tipo = "No aplica"
            elif 15 <= rec.edad <= 16:
                tipo = "Cadete"
            elif 17 <= rec.edad <= 21:
                tipo = "Junior"
            elif rec.edad >= 50:
                tipo = "Senior"
            elif rec.edad >= 22:
                tipo = "Mayor"
            rec.tipo_membresia_auto = tipo

            # Buscar la membresía correspondiente en la base de datos
            membresia = self.env['golf.membership.type'].search([('name', '=', tipo)], limit=1)
            rec.tipo_membresia_id = membresia if membresia else False
