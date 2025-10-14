# Procedimiento Operativo Estándar (SOP)
## Falla de Impresora de Boletas en Terminal de Punto de Venta (POS)

---

### 1. Propósito
Definir el procedimiento para diagnosticar y resolver fallas en la impresora fiscal/de boletas asociada a un terminal POS, garantizando la continuidad de la operación en caja y el cumplimiento de requisitos legales de emisión de documentos tributarios.

---

### 2. Alcance
Aplica a:
- Todas las impresoras fiscales/de boletas conectadas a terminales POS en tiendas físicas.  
- Personal de caja y supervisores.  
- Mesa de ayuda (soporte técnico nivel 1).  

---

### 3. Responsables
- **Cajero/a:** Identificar y reportar la falla inmediatamente.  
- **Supervisor/a de Tienda:** Validar ejecución del procedimiento.  
- **Mesa de Ayuda Nivel 1:** Asistir en la resolución remota y escalar a Nivel 2 si persiste.  

---

### 4. Definiciones
- **Impresora de boletas:** Dispositivo fiscal obligatorio para impresión de comprobantes.  
- **RTO:** Tiempo máximo aceptable de recuperación (10 min).  
- **RPO:** Pérdida máxima de boletas tolerable: ninguna (documentos deben quedar registrados).  

---

### 5. Precondiciones
- La caja presenta error al imprimir boleta o mensaje de impresora no disponible.  
- El papel fiscal está correctamente cargado y no caducado.  
- El terminal POS está encendido y funcionando.  

---

### 6. Procedimiento

#### Paso 1: Verificación física
1. Compruebe que la impresora esté encendida (luz de “Power” activa).  
2. Verifique que el cable de energía esté correctamente conectado.  
3. Revise conexión del cable USB o serial al terminal POS.  
4. Asegúrese de que el rollo de papel esté colocado correctamente y que el sensor detecte papel.  

**Tiempo estimado:** 3 minutos  
**Criterio de éxito:** Impresora lista (luz verde encendida, sin alertas).  

---

#### Paso 2: Reinicio de la impresora
1. Apague la impresora.  
2. Espere 30 segundos.  
3. Enciéndala nuevamente.  
4. Observe que realice el ciclo de inicialización sin errores.  

**Tiempo estimado:** 2 minutos  
**Criterio de éxito:** La impresora se inicializa y queda “Ready”.  

---

#### Paso 3: Validación desde el POS
1. En el terminal POS, acceda a **Configuración > Dispositivos > Impresora Fiscal**.  
2. Ejecute **Imprimir página de prueba**.  
3. Valide que la página de prueba salga correctamente.  

**Tiempo estimado:** 2 minutos  
**Criterio de éxito:** Página de prueba emitida sin errores.  

---

#### Paso 4: Reinstalación de driver (si falla prueba)
1. Desde el POS, abra **Administrador de dispositivos**.  
2. Localice la impresora en la lista.  
3. Desinstale y reinstale el controlador.  
4. Reinicie el POS.  

**Tiempo estimado:** 5 minutos  
**Criterio de éxito:** Impresora reconocida y lista en el sistema.  

---

#### Paso 5: Escalamiento a mesa de ayuda
Si después de los pasos anteriores la impresora sigue sin funcionar:  
1. Registre ticket en la Mesa de Ayuda categoría **Printer Issue / Impresora Fiscal**.  
2. Incluya:  
   - Código de caja y tienda.  
   - Número de serie de la impresora.  
   - Hora exacta del incidente.  
   - Acciones realizadas según este SOP.  
3. Mesa de ayuda validará logs y, si corresponde, escalará a proveedor externo.  

**Tiempo estimado:** 5 minutos.  

---

### 7. Tiempo total estimado
- Verificación física: 3 min  
- Reinicio: 2 min  
- Validación prueba: 2 min  
- Reinstalación driver: 5 min  
- Escalamiento: 5 min  

**RTO esperado:** ≤ 10–15 min  
**RPO esperado:** 0 (todas las boletas deben emitirse).  

---

### 8. Referencias
- Manual de Impresora Fiscal Modelo X (Doc FISC-2024).  
- Política de Continuidad Operativa de Tienda (CO-2024).  

---

### 9. Control de cambios
- **Versión 1.0 (2025-08-29):** Creación inicial del procedimiento.  
