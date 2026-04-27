# ESTADO DEL PROYECTO: COMPARADOR GESTION GROUP

Este documento resume la evolución del proyecto, las mejoras de seguridad implementadas y los pasos necesarios para alcanzar la versión de producción.

## 🏁 1. Tareas Realizadas (Auditoría y Remediación)

### 🔒 Seguridad y Arquitectura
- **Protección de IP**: Se ha movido el motor de cálculo de comisiones al backend (Python). Ya no es visible en el navegador.
- **Seguridad de Acceso**: Implementado hashing de contraseñas con **bcrypt**.
- **Gestión de Sesiones**: Tokens de sesión seguros con expiración de 24h y auto-limpieza.
- **Protección de Secretos**: Whitelist en `/api/config` para no exponer API Keys de IA.

### ⚡ Rendimiento
- **Vercel Native Static**: Los archivos HTML/JS/CSS se sirven desde `/public` para una velocidad de carga máxima.
- **Firestore Optimizada**: Consultas con límites de seguridad para evitar costes excesivos.

---

## 🚀 2. Hoja de Ruta (Roadmap)

### 🥇 PRIORIDAD: Tarifas 2.0 TD (Residencial/Pymes)
- [ ] **Pruebas de estrés**: Verificar la lógica de ahorro en facturas 2.0 reales.
- [ ] **Autoconsumo**: Implementar y probar el funcionamiento de la **Batería Virtual** y compensación de excedentes.
- [ ] **Ajuste de Precios**: Revisar que el cambio P2 -> P3 en 2.0 (si aplica) sea automático y correcto.

### 🥈 Fase 2: Tarifas Industriales (3.0 y 6.1)
- [ ] **Validación 3.0**: Probar comparativas con 6 periodos de potencia asimétrica.
- [ ] **Validación 6.1**: Pruebas con rangos de alta tensión.

### 🎨 Visual y Experiencia de Usuario
- [ ] **Pulido de Comisiones**: Ajustar la interfaz de administración para tramos complejos.
- [ ] **PDF de Lujo**:
    - [ ] Mejorar la salida visual con colores corporativos (Paleta Gestion Group).
    - [ ] Insertar logo de la empresa en alta resolución.
    - [ ] Refinar tablas comparativas para que sean más legibles.

### 🔗 Integración con CRM (https://crm.gestiongroup.es/)
- [ ] **Estudio de API**: Analizar la vía de comunicación con el CRM propio.
- [ ] **Sincronización**: Vincular los estudios generados directamente con la ficha del cliente en el CRM.

---

## 🛠️ 3. Guía de Despliegue (Git)

Para subir cualquier cambio realizado localmente:

1. `git add .`
2. `git commit -m "Descripción del cambio"`
3. `git push`

---
*Documento generado el 27 de Abril de 2026 por Antigravity (Advanced Agentic Coding).*
