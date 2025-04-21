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

    show_golf_extras = fields.Boolean(compute="_compute_visibility", store=True)
    show_lesson_type = fields.Boolean(compute="_compute_visibility", store=True)
    show_instructor = fields.Boolean(compute="_compute_visibility", store=True)
    show_school = fields.Boolean(compute="_compute_visibility", store=True)

    @api.model
    def _get_day_condition(self, dt):
        return 'weekend' if dt.weekday() >= 5 else 'laborable'

    @api.depends('booking_datetime', 'booking_type', 'member_id', 'has_buggy', 'has_locker', 'has_parking')
    def _compute_price(self):
        for rec in self:
            rec.price = 0.0
            if not rec.member_id or not rec.booking_datetime or not rec.booking_type:
                continue

            # Día: laborable o festivo
            condition = rec._get_day_condition(rec.booking_datetime)

            # Tipo de usuario
            abono = rec.member_id.tipo_membresia_id
            if not abono:
                user_type = 'no_abonado'
            elif abono.code == 'BIRDIE':
                user_type = 'birdie'
            elif abono.code == 'HOI':
                user_type = 'hole_in_one'
            else:
                user_type = 'club'  

            # Tipo de servicio principal
            rate_type = rec.booking_type

            # Green Fee
            if rate_type == 'green_fee':
                green_fee = self.env['golf.fee.rate'].search([
                    ('type', '=', 'green_fee'),
                    ('user_type', '=', user_type),
                    ('condition', '=', condition),
                    ('active', '=', True)
                ], limit=1)
                if green_fee:
                    rec.price += green_fee.price
                
            elif rate_type == 'school' and rec.school_condition:
                fee = self.env['golf.fee.rate'].search([
                    ('type', '=', 'school'),
                    ('user_type', '=', user_type),
                    ('condition', '=', rec.school_condition),
                    ('active', '=', True)
                ], limit=1)
                if fee:
                    rec.price += fee.price

            # Campo de prácticas u otros
            elif rate_type in ['practice', 'lesson', 'fitting', 'other']:
                fee = self.env['golf.fee.rate'].search([
                    ('type', '=', rate_type),
                    ('user_type', '=', user_type),
                    ('condition', '=', condition),
                    ('active', '=', True)
                ], limit=1)
                if fee:
                    rec.price += fee.price

            # Complementos
            if rec.has_buggy:
                buggy_fee = self.env['golf.fee.rate'].search([
                    ('type', '=', 'buggy'),
                    ('user_type', '=', user_type),
                    ('condition', '=', condition),
                    ('active', '=', True)
                ], limit=1)
                if buggy_fee:
                    rec.price += buggy_fee.price

            if rec.has_locker:
                locker_fee = self.env['golf.fee.rate'].search([
                    ('type', '=', 'locker'),
                    ('user_type', '=', user_type),
                    ('condition', '=', 'otros'),
                    ('active', '=', True)
                ], limit=1)
                if locker_fee:
                    rec.price += locker_fee.price

            if rec.has_parking:
                parking_fee = self.env['golf.fee.rate'].search([
                    ('type', '=', 'parking'),
                    ('user_type', '=', user_type),
                    ('condition', '=', 'otros'),
                    ('active', '=', True)
                ], limit=1)
                if parking_fee:
                    rec.price += parking_fee.price

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
                
    @api.depends('booking_type', 'lesson_type')
    def _compute_visibility(self):
        for rec in self:
            rec.show_golf_extras = rec.booking_type == 'green_fee'
            rec.show_lesson_type = rec.booking_type == 'lesson'
            rec.show_instructor = (
                rec.booking_type == 'fitting' or
                (rec.booking_type == 'lesson' and rec.lesson_type == 'individual')
            )
            rec.show_school = rec.booking_type == 'school'


