# 🏌️‍♂️ Don Tello Club de Golf - Odoo Module

Este repositorio contiene el desarrollo del módulo `don_tello` para la gestión del Club de Golf **Don Tello**, desarrollado sobre Odoo 16.

---

## 📁 Estructura del proyecto

```
addons/
├── don_tello/
│   ├── models/...
│   ├── views/...
│   ├── __manifest__.py
│   └── 
```

---

## 👥 Equipo y ramas

| Desarrollador | Rama de desarrollo     |
|---------------|------------------------|
| Adrian         | `dev/adria`            |
| Pablo         | `dev/pablo`            |
| Producción    | `main` (vía Pull Request) |

---

## 🚀 Primeros pasos para empezar a trabajar

### 1. Clona el repositorio

```bash
git clone https://github.com/adrmurbau/odoo-don-tello.git
cd odoo-don-tello
```

> ⚠️ Asegúrate de tener acceso al repositorio en GitHub (comunícate con Adrian si no lo tienes).

---

### 2. Cambia a tu rama de desarrollo

```bash
git checkout dev/pablo
```

> En esta rama harás todos tus cambios. Nunca trabajes directamente sobre `main`.

---

### 3. Añade tus cambios

```bash
# Añadir archivos modificados
git add .

# Commit con un mensaje claro
git commit -m "feat: añade formulario de reservas"

# Sube tus cambios
git push origin dev/pablo
```

---

### 4. Mantén tu rama actualizada

De vez en cuando, trae los últimos cambios de `main`:

```bash
git checkout dev/pablo
git pull origin main
```

> ⚠️ Si hay conflictos, resuélvelos antes de seguir trabajando.

---

## ✅ Flujo de trabajo

1. Trabajas en `dev/pablo`.
2. Cuando termines una funcionalidad estable, **avisas a Adrian o haces un Pull Request hacia `main`**.
3. Se revisa y se hace merge solo si todo funciona correctamente.

---

## 📦 Requisitos

- Odoo 16
- PostgreSQL
- Git
- Python ≥ 3.10

---

## 🆘 Ayuda

Si tienes cualquier duda:
- Contacta con **Adria** (compañero principal).
- Consulta la documentación del módulo.
- Pregunta en los issues del repositorio si es algo general.

---

