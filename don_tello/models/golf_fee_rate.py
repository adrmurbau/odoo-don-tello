from odoo import models, fields

class GolfFeeRate(models.Model):
    _name = 'golf.fee.rate'
    _description = 'Tarifa Oficial del Club Don Tello'

    name = fields.Char(string="Nombre de la Tarifa", required=True)
    code = fields.Char(string="Código Interno")
    
    type = fields.Selection([
        ('membership', 'Abonos'),
        ('addon', 'Complementos de Abonos'),
        ('game_rights', 'Derechos de Juego'),
        ('green_fee', 'Green Fee'),
        ('buggy', 'Alquiler de Buggy'),
        ('locker', 'Taquillas'),
        ('parking', 'Parking'),
        ('practice', 'Campo de Prácticas'),
        ('lesson', 'Clases'),
        ('school', 'Escuelas Deportivas'),
        ('fitting', 'Fitting'),
        ('other', 'Otros Servicios'),
    ], string="Categoría", required=True)

    user_type = fields.Selection([
        ('abonado', 'Abonado'),
        ('no_abonado', 'No Abonado'),
        ('hijo', 'Hijo'),
        ('invitado', 'Invitado'),
        ('general', 'General'),
        ('club', 'Abono Club'),
        ('hole_in_one', 'Abono Hole In One'),
        ('birdie', 'Abono Birdie'),
    ], string="Tipo de Usuario", default='general')

    condition = fields.Selection([
        ('laborable', 'Laborables'),
        ('weekend', 'Fines de semana y festivos'),
        ('otros', 'Otros'),
        ('individual', 'Clase individual'),
        ('bono', 'Bono 12 clases'),
        ('group', 'Grupo infantil'),
        ('1_clase_1h_grupo', '1 clase semanal (1h grupo)'),
        ('2_clases_1h_grupo', '2 clases semanales (1h grupo)'),
        ('1_clase_1h_3pax', '1 clase semanal (1h, grupo 3pax)'),
        ('1_clase_1h_4pax', '1 clase semanal (1h, grupo 4pax)'),
        ('consulta', 'Consultar'),
        ('primer_jugador', '1er Jugador'),
    ], string="Condición", default='laborable')

    price = fields.Float(string="Precio (€)", required=True)
    notes = fields.Text(string="Notas Adicionales")
    active = fields.Boolean(string="Activo", default=True)
