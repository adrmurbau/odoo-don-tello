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
    ('weekend', 'Finde/Festivos'),
    ('hijo_25_29', 'Hijo/a 25-29 años'),
    ('hijo_30_34', 'Hijo/a 30-34 años'),
    ('primer_jugador', '1er Jugador'),
    ('segundo_jugador', '2º Jugador'),
    ('hijos', 'Hijo/s'),
    ('progresion_1er_ano', 'Progresión 1er Año'),
    ('progresion_2do_ano', 'Progresión 2º Año'),
    ('grupo_3', 'Grupo 3 personas'),
    ('grupo_4', 'Grupo 4 personas'),
    ('bono', 'Bono 12 clases'),
    ('individual', 'Clase individual'),
    ('consulta', 'Consultar'),
    ('plan_birdie', 'Plan Birdie'),
    ('hole_in_one', 'Hole in One'),
    ('1_clase_1h_grupo', '1 clase semanal 1h en grupo'),
    ('2_clases_1h_grupo', '2 clases semanales de 1h en grupo'),
    ('1_clase_1h_3pax', '1 clase semanal 1h grupo de 3pax'),
    ('1_clase_1h_4pax', '1 clase semanal 1h grupo de 4pax'),
    ('general', 'General'),
    ('otros', 'Otros'),
    ('sin_condicion', 'Sin condición'),
    ], string="Condición", default='sin_condicion')

    price = fields.Float(string="Precio (€)", required=True)
    notes = fields.Text(string="Notas Adicionales")
    active = fields.Boolean(string="Activo", default=True)
