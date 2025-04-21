from odoo import models, fields

class GolfMembershipType(models.Model):
    _name = 'golf.membership.type'
    _description = 'Tipo de Membresía del Club'

    name = fields.Char(string='Nombre', required=True)
    code = fields.Char(string='Código Interno')  # ej: CLUB, HOI, BIRDIE

    # Cuotas
    monthly_fee = fields.Float(string='Cuota Mensual')
    promo_fee = fields.Float(string='Cuota Promocional')
    promo_months = fields.Integer(string='Meses con Cuota Promocional')
    annual_fee = fields.Float(string='Cuota Anual Opcional')
    payment_type = fields.Selection([
        ('mensual', 'Mensual'),
        ('anual', 'Anual'),
        ('ambos', 'Ambos')
    ], string='Tipo de Pago', default='mensual')

    # Derechos y acceso
    club_rights_exempt = fields.Boolean(string='Exento de derechos de club (595€)', default=True)
    includes_family = fields.Boolean(string='Incluye Unidad Familiar')
    max_children_age = fields.Integer(string='Edad máxima de hijos incluidos', default=24)
    access_pool = fields.Boolean(string='Acceso a Piscina')
    access_camps = fields.Boolean(string='Inscripción a Campamentos')
    access_golf_practice = fields.Boolean(string='Campo de Prácticas de Golf')
    access_adult_school = fields.Boolean(string='Escuela de Golf Adultos')
    access_kids_school = fields.Boolean(string='Escuelas Deportivas Infantiles')
    sports = fields.Many2many('golf.sport', string='Escuelas Deportivas Incluidas')
    access_golf_course = fields.Boolean(string='Acceso a Campo de Golf')

    # Derechos de juego
    game_rights_type = fields.Selection([
        ('none', 'No Incluidos'),
        ('progressive', 'En Progresión'),
        ('included', 'Incluidos'),
    ], string='Derechos de Juego')

    # Bonificaciones y restricciones
    has_discount_rights = fields.Boolean(string='Con derecho a bonificaciones')
    has_invitation_rights = fields.Boolean(string='Puede invitar a terceros')
    max_invitations_per_year = fields.Integer(string='Máximo de Invitaciones / Año')
    access_locker = fields.Boolean(string='Incluye acceso a taquilla')
    locker_type = fields.Selection([
        ('ninguna', 'Ninguna'),
        ('pequena', 'Pequeña'),
        ('grande', 'Grande')
    ], string='Tipo de Taquilla Incluida', default='ninguna')
    includes_parking = fields.Boolean(string='Incluye plaza de parking para buggy')

    # Estados y notas
    is_promotional = fields.Boolean(string='Es un abono promocional', default=False)
    color = fields.Integer(string="Color", help="Color para distinguir en vistas kanban")
    notes = fields.Text(string='Notas')
    active = fields.Boolean(default=True)
