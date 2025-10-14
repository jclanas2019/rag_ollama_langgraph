# Procedimiento Operativo Estándar (SOP)
## Reinicio de Terminal de Punto de Venta (POS)

---

### 1. Propósito
Establecer un procedimiento estandarizado para reiniciar un terminal de Punto de Venta (POS) cuando presenta fallas de software, congelamiento o lentitud, con el fin de minimizar el Tiempo de Recuperación (RTO) y asegurar la continuidad operativa en caja.

---

### 2. Alcance
Este procedimiento aplica a:
- Todos los terminales POS de las tiendas físicas.  
- Personal de caja y personal de soporte de primera línea (mesa de ayuda).  

No aplica a equipos administrativos o terminales de back office.

---

### 3. Responsables
- **Cajero/a:** Detectar y reportar incidentes de congelamiento o lentitud.  
- **Supervisor/a de Tienda:** Validar que el procedimiento se ejecute correctamente.  
- **Mesa de Ayuda Nivel 1:** Asistir remotamente y escalar si el problema persiste.  

---

### 4. Definiciones
- **RTO (Recovery Time Objective):** Tiempo máximo de recuperación aceptable (10 min para POS).  
- **RPO (Recovery Point Objective):** Pérdida máxima de datos tolerable (5 min en transacciones).  
- **POS Congelado:** Equipo no responde a teclado, mouse ni comandos de software.

---

### 5. Precondiciones
- El cajero debe haber guardado o anotado manualmente la última transacción si estaba en curso.  
- Se debe contar con acceso físico al terminal POS.  
- Conexión eléctrica estable y periféricos (impresora fiscal, gaveta de dinero) conectados.  

---

### 6. Procedimiento

#### Paso 1: Identificación inicial
1. Confirme que el POS no responde a teclado o mouse.  
2. Si responde parcialmente, intente cerrar la aplicación de caja desde el menú.  
3. Si el POS está completamente bloqueado, proceda al Paso 2.

#### Paso 2: Reinicio de la aplicación POS
1. Presione `Shift + F12` para forzar el cierre de la aplicación.  
2. Espere 30 segundos.  
3. Vuelva a abrir la aplicación **Caja POS** desde el acceso directo en el escritorio.  
4. Valide si la aplicación inicia correctamente.  

**Tiempo estimado:** 2 minutos  
**Criterio de éxito:** La aplicación inicia y permite procesar transacciones.  

#### Paso 3: Reinicio completo del equipo
1. Presione `Ctrl + Alt + Supr` y seleccione **Reiniciar**.  
2. Si no responde, mantenga presionado el botón de encendido durante 10 segundos hasta que el equipo se apague.  
3. Encienda nuevamente el terminal.  
4. Una vez cargado Windows, abra la aplicación **Caja POS**.  

**Tiempo estimado:** 5 minutos  
**Criterio de éxito:** El equipo inicia sin errores y la aplicación funciona normalmente.  

#### Paso 4: Validación de conectividad
1. Verifique que el POS se conecte al servidor de base de datos (el sistema debe mostrar el estado “En línea”).  
2. Ejecute una transacción de prueba (anulación inmediata).  
3. Compruebe que la impresora fiscal emite la boleta y que la gaveta de dinero abre correctamente.  

**Tiempo estimado:** 3 minutos  
**Criterio de éxito:** Transacción de prueba registrada en el sistema central.  

---

### 7. Escalamiento
- Si después de completar el Paso 3 el POS sigue sin responder, registre un **ticket en la Mesa de Ayuda** con categoría **Software Hang / Congelado**.  
- Incluya:  
  - Código de caja y número de tienda.  
  - Hora exacta del incidente.  
  - Mensajes de error en pantalla (si los hubo).  
  - Acciones realizadas según este SOP.  

---

### 8. Tiempo total estimado
- Reinicio de aplicación: ~2 min.  
- Reinicio completo + validación: ~10 min.  
- Escalamiento a mesa de ayuda: +5 min (registro de ticket).  

---

### 9. Referencias
- Manual de Usuario POS v3.2  
- Política de Continuidad Operativa de Tienda (Documento CO-2024)  

---

### 10. Control de cambios
- **Versión 1.0 (2025-08-29):** Creación inicial del procedimiento.  
