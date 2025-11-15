# ⛳ Don Tello Club de Golf – Módulo Odoo 16

Este repositorio contiene el desarrollo del módulo **`don_tello`** para la gestión del **Club de Golf Don Tello**, construido sobre **Odoo 16**.

El objetivo del proyecto es crear un módulo **profesional, escalable y fiel a las tarifas y servicios reales del club**, gestionando socios, cuotas, reservas, escuelas deportivas y eventos desde un único sistema.

---

## 🧩 Funcionalidades principales

### 👥 Gestión de socios (`golf.member`)
- Alta y gestión de socios del club.
- Datos personales, contacto, estado de la membresía y fecha de alta/baja.
- Cálculo y clasificación automática del socio según:
  - Edad.
  - Condición de jugador de golf.
  - Reglas de negocio del club (cadete, junior, mayor, senior, no jugador).

### 💳 Tipos de membresía (`golf.membership.type`)
- Definición de distintos tipos de socios y cuotas asociadas.
- Configuración de:
  - Modalidad de pago (mensual, anual, etc.).
  - Acceso a servicios adicionales: taquillas, parking, invitaciones, descuentos.
  - Bonificaciones y condiciones especiales.

### 💰 Tarifas oficiales (`golf.fee.rate`)
- Modelado de todas las tarifas oficiales del club:
  - Abonos (Club, Hole in One, Birdie…).
  - Green fees y derechos de juego.
  - Buggy.
  - Taquillas.
  - Fitting.
  - Escuelas deportivas.
  - Alquiler de pistas (tenis, pádel, etc.).
- Condiciones según:
  - Tipo de usuario (abonado / no abonado).
  - Día laborable vs. fin de semana/festivo.
  - Otros criterios definidos en el modelo.

### 📅 Reservas unificadas (`golf.booking`)
- Modelo único para gestionar:
  - Green fee.
  - Campo de prácticas.
  - Clases de golf.
  - Fitting.
  - Escuelas deportivas.
- Cálculo automático de precios combinando:
  - Tipo de reserva.
  - Tipo de socio.
  - Día (laborable/festivo).
  - Servicios asociados (buggy, taquilla, parking…).
- Control básico de solapamientos y disponibilidad.

### 🎟️ Eventos y control de asistencia
- Gestión de eventos del club (torneos, clinics, actividades especiales).
- Control de asistencia de socios mediante wizard de **check-in / check-out**.
- Restricción de selección de participantes a socios inscritos en el evento.

### 🏫 Escuelas deportivas (`golf.sport`)
- Definición de actividades deportivas ofrecidas por el club.
- Integración con reservas y posibles tarifas específicas.

---

## 🛠️ Stack tecnológico

- **Odoo 16** (Community Edition).
- **Python 3.10+**.
- **PostgreSQL**.
- Vistas y datos en **XML** (`views/`, `data/`, `security/`).
- Control de versiones con **Git** y flujo de trabajo por ramas.

---

## 📂 Estructura del repositorio

```text
.
├── don_tello/
│   ├── models/
│   │   ├── golf_member.py
│   │   ├── golf_membership_type.py
│   │   ├── golf_fee_rate.py
│   │   ├── golf_booking.py
│   │   └── ...
│   ├── views/
│   │   ├── golf_member_views.xml
│   │   ├── golf_membership_type_views.xml
│   │   ├── golf_fee_rates_views.xml
│   │   ├── golf_booking_views.xml
│   │   └── ...
│   ├── security/
│   │   ├── ir.model.access.csv
│   │   └── security.xml
│   ├── data/
│   │   ├── membership_type_data.xml
│   │   ├── fee_rate_data.xml
│   │   ├── sport_data.xml
│   │   └── ...
│   ├── __manifest__.py
│   └── __init__.py
│
├── estate/
│   └── ... (módulo de ejemplo de Odoo utilizado como referencia)
│
├── .tx/
├── .gitignore
└── README.md
````

> La estructura puede evolucionar a medida que se amplían modelos, vistas y datos, pero el núcleo del módulo reside siempre en `don_tello/`.

---

## 🌱 Cómo empezar (instalación básica)

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/adrmurbau/odoo-don-tello.git
   cd odoo-don-tello
   ```

2. Asegurarse de que la ruta a este repositorio está incluida en el `addons_path` de tu configuración de Odoo (`odoo.conf`), por ejemplo:

   ```ini
   addons_path = /ruta/a/tus/addons,/ruta/a/odoo-don-tello
   ```

3. Reiniciar el servidor de Odoo.

4. Desde la interfaz web de Odoo:

   * Ir a **Aplicaciones**.
   * Actualizar la lista de módulos.
   * Buscar **Don Tello Club de Golf** o `don_tello`.
   * Instalar el módulo.

---

## 🔁 Flujo de trabajo con Git

Este repositorio está pensado para trabajo en equipo utilizando ramas dedicadas:

* `dev/adria` → rama de desarrollo de Adrián.
* `dev/pablo` → rama de desarrollo de Pablo.
* `main` → rama estable (producción), actualizada solo mediante Pull Requests.

### 1. Clonar el repositorio

```bash
git clone https://github.com/adrmurbau/odoo-don-tello.git
cd odoo-don-tello
```

### 2. Cambiar a tu rama de desarrollo

Ejemplos:

```bash
git checkout dev/adria
# o
git checkout dev/pablo
```

> Todos los cambios de desarrollo se hacen en tu rama. **Nunca** se trabaja directamente sobre `main`.

### 3. Añadir y subir cambios

```bash
# Añadir archivos modificados
git add .

# Crear un commit con un mensaje claro
git commit -m "feat: añade formulario de reservas"

# Subir la rama al remoto
git push origin dev/adria
```

### 4. Mantener tu rama actualizada con `main`

Periódicamente:

```bash
git checkout dev/adria
git pull origin main
```

Resolver conflictos si los hubiera y hacer nuevos commits si es necesario.

### 5. Integración en `main`

1. Cuando una funcionalidad esté estable:

   * Se crea un **Pull Request** desde `dev/adria` o `dev/pablo` hacia `main`.
2. Se revisa el código y se realizan pruebas.
3. Solo si todo funciona correctamente, se hace **merge** a `main`.

---

## ✅ Requisitos

* Odoo **16** instalado y configurado.
* Servidor de base de datos **PostgreSQL**.
* **Python 3.10+**.
* **Git** para clonar el repositorio y gestionar ramas.

---

## 👤 Mi rol en el proyecto

* Diseño funcional y técnico del módulo **`don_tello`**.
* Implementación de los modelos principales:

  * `golf.member`, `golf.membership.type`, `golf.fee.rate`, `golf.booking`, `golf.sport`, entre otros.
* Desarrollo de la lógica de negocio para:

  * Cálculo de precios en reservas según tipo de socio, tipo de reserva y día.
  * Clasificación automática de socios según edad y condición de jugador.
* Definición de vistas (formularios, listas, menús) y wizards específicos.
* Creación de datos iniciales (tipos de membresía, tarifas oficiales, deportes).
* Configuración del flujo de trabajo con Git y coordinación de ramas de desarrollo.

---

## ❓ Ayuda y soporte

Si tienes dudas o quieres saber más sobre el proyecto:

* Abre un **issue** en este repositorio.
* Contacta con **Adrián Muriel**:

  * GitHub: [@adrmurbau](https://github.com/adrmurbau)
  * Email: adrianmb41[at]gmail.com

```
