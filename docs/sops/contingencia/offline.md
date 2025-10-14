# Contingencia de ventas en modo Offline

**Cuándo usar:** Cuando el POS indica **“Sin conexión”** y la prueba de red **falla**.

## Activación
1. En el POS: **Menú → Modo Offline → Activar**.
2. Confirmar que aparece el indicador **“Offline”** en pantalla.

## Registro de ventas
- Registrar cada venta como **pendiente** (el POS creará un folio temporal).
- Conservar **comprobantes** y/o notas manuales si el sistema lo requiere.

## Límites
- Máximo **N** ventas offline por POS *(configurable)*.
- No procesar **devoluciones** hasta volver online.

## Al volver la red
1. En el POS: **Menú → Sincronizar pendientes**.
2. Verificar que todas las ventas queden **“Sincronizadas”**.
3. Si alguna queda en **error**, escalar con **ID POS + folio**.

## Riesgos y controles
- **Duplicados:** el POS debe evitar doble registro al sincronizar.
- **Medios de pago:** seguir las políticas del emisor si aplica autorización manual.
