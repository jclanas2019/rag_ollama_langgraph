# SOP: Red caída en POS

**Perfil:** Usuario de caja / supervisor de tienda  
**Objetivo:** Restablecer conectividad del POS en ~3 minutos o activar contingencia para continuar vendiendo.

## Indicadores en pantalla
- Mensaje: “Sin conexión” o “Fallo de red”.
- Botón disponible: **Probar red**.

## Pasos inmediatos (≈3 min)

1. **Verificación rápida (60 s)**
   - Confirmar **cable de red** firme en POS y switch (Leds encendidos).
   - Si es **Wi-Fi**, verificar que el POS está conectado a la **red de la tienda**.

2. **Reiniciar conexión (60–90 s)** *(sin clientes pagando)*
   - Desconectar y reconectar cable de red del POS.
   - Reiniciar **router y switch**. Esperar **60 s**.

3. **Prueba (30 s)**
   - Pulsar **Probar red**. Resultado esperado: **“Conectado”**.

## Si NO se restablece
- Activar **Modo Offline** del POS.
- Registrar ventas como **pendientes de sincronizar**.
- Cuando vuelva la red: **Menú → Sincronizar pendientes**.

## Escalamiento
Abrir ticket desde la opción **Escalar** y adjuntar:
- Tienda, **ID POS**, hora del incidente.
- Pasos ejecutados y resultado de **Probar red**.
- Foto de **router/switch** mostrando luces.
- Teléfono de contacto.

## Seguridad / Notas
- No manipular cableado si hay **riesgo eléctrico**.
- No reiniciar equipos con **pagos en curso**.
- Mantener el **talonario** o registro offline accesible.

## SLA sugerido
- Restaurar en tienda: **≤ 5 min**.  
- Soporte central: **≤ 15 min** desde el ticket.

## Referencias
- `docs/checklists/red_fisico.md`
- `docs/contingencia/offline.md`
