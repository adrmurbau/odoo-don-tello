from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

class GolfBooking(models.Model):
    _name = 'golf.booking'
    _description = 'Reserva de Instalaciones'

    member_id = fields.Many2one(comodel_name='golf.member', string='Socio', required=True)
    name = fields.Char(string="Referencia", required=True, default="Reserva")

    booking_datetime = fields.Datetime(string='Fecha de Reserva', required=True)
    booking_type = fields.Selection([
        ('green_fee','Green Fee'),
        ('practice','Prácticas'),
        ('school','Otros deportes'),
        ('lesson','Clase de Golf'),
        ('fitting','Fitting'),
    ], string='Tipo', required=True)

    price = fields.Float(
        string='Precio Aplicado (€)',
        compute='_compute_price',
        store=True,
        readonly=True,
    )
    has_buggy = fields.Boolean(string="¿Incluye buggy?")
    has_locker = fields.Boolean(string="¿Taquilla?")
    has_parking = fields.Boolean(string="¿Parking buggy?")

    # Para clases de golf
    lesson_type = fields.Selection([
        ('group', 'Clase en grupo'),
        ('individual', 'Clase individual'),
        ('bono', 'Bono 12 clases'),
    ], string="Tipo de Clase")

    instructor_id = fields.Many2one(
        'golf.staff',
        string="Instructor",
        domain="[('department', '=', 'golf')]" 
    )

    school_condition = fields.Selection([
        ('1_clase_1h_grupo', 'Equitación (1h/sem)'),
        ('2_clases_1h_grupo', 'Equitación (2h/sem)'),
        ('1_clase_1h_3pax', 'Padel/Tenis (grupo 3 pax)'),
        ('1_clase_1h_4pax', 'Padel/Tenis (grupo 4 pax)'),
    ], string="Modalidad Escuela Deportiva")

    has_buggy = fields.Boolean(string="¿Incluir buggy?")
    has_locker = fields.Boolean(string="¿Incluir taquilla?")
    has_parking = fields.Boolean(string="¿Incluir parking?")

    @api.model
    def _get_day_condition(self, dt):
        return 'weekend' if dt.weekday() >= 5 else 'laborable'

    @api.depends(
    'booking_datetime', 'booking_type', 'member_id',
    'has_buggy', 'has_locker', 'has_parking',
    'school_condition', 'lesson_type'
    )
    def _compute_price(self):
        for rec in self:
            rec.price = 0.0

            if not rec.member_id or not rec.booking_datetime or not rec.booking_type:
                continue

            # Tipo de usuario real
            abono = rec.member_id.tipo_membresia_id
            if not abono:
                user_type = 'no_abonado'
            elif abono.code == 'BIRDIE':
                user_type = 'birdie'
            elif abono.code == 'HOI':
                user_type = 'hole_in_one'
            else:
                user_type = 'club'

            # Condición del día
            condition = 'weekend' if rec.booking_datetime.weekday() >= 5 else 'laborable'

            # Fitting siempre tarifa 0
            if rec.booking_type == 'fitting':
                rec.price = 0.0
                continue

            # Si es lesson o school → usar 'abonado' como user_type
            if rec.booking_type in ['lesson', 'school']:
                user_type_tarifa = 'abonado'
            else:
                user_type_tarifa = user_type

            # Dominio para buscar tarifa base
            domain = [
                ('type', '=', rec.booking_type),
                ('user_type', '=', user_type_tarifa),
                ('active', '=', True)
            ]

            if rec.booking_type == 'lesson':
                if not rec.lesson_type:
                    continue
                domain.append(('condition', '=', rec.lesson_type))

            elif rec.booking_type == 'school':
                if not rec.school_condition:
                    continue
                domain.append(('condition', '=', rec.school_condition))

            else:
                domain.append(('condition', '=', condition))

            tarifa = self.env['golf.fee.rate'].search(domain, limit=1)
            if tarifa:
                rec.price += tarifa.price

            # Extras solo aplican si es green_fee
            if rec.booking_type == 'green_fee':
                user_type_extra = 'abonado'

                if rec.has_buggy:
                    buggy = self.env['golf.fee.rate'].search([
                        ('type', '=', 'buggy'),
                        ('user_type', '=', user_type_extra),
                        ('condition', '=', condition),
                        ('active', '=', True)
                    ], limit=1)
                    if buggy:
                        rec.price += buggy.price

                if rec.has_locker:
                    locker = self.env['golf.fee.rate'].search([
                        ('type', '=', 'locker'),
                        ('user_type', '=', user_type_extra),
                        ('condition', '=', 'otros'),
                        ('active', '=', True)
                    ], limit=1)
                    if locker:
                        rec.price += locker.price

                if rec.has_parking:
                    parking = self.env['golf.fee.rate'].search([
                        ('type', '=', 'parking'),
                        ('user_type', '=', user_type_extra),
                        ('condition', '=', 'otros'),
                        ('active', '=', True)
                    ], limit=1)
                    if parking:
                        rec.price += parking.price

    @api.constrains('booking_datetime', 'instructor_id')
    def _check_instructor_availability(self):
        for rec in self:
            if rec.booking_type in ['lesson', 'fitting'] and rec.instructor_id:
                overlapping = self.search([
                    ('id', '!=', rec.id),
                    ('booking_datetime', '=', rec.booking_datetime),
                    ('instructor_id', '=', rec.instructor_id.id),
                ])
                if overlapping:
                    raise ValidationError("El instructor ya tiene otra reserva en ese horario.")
                


