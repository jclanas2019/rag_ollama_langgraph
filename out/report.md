# Reporte de Frecuencia de Términos

## escaner.md

| Término | Frecuencia |
|---|---:|
| checklist | 1 |
| escáner | 1 |
| lente | 1 |
| limpio | 1 |
| golpes | 1 |
| cable | 1 |
| usb | 1 |
| firme | 1 |

**Resumen LLM (gemma3:1b):**
(Texto breve: se omite resumen LLM.)

## impresora_termica.md

| Término | Frecuencia |
|---|---:|
| luz | 2 |
| checklist | 1 |
| impresora | 1 |
| térmica | 1 |
| papel | 1 |
| térmico | 1 |
| correcto | 1 |
| orientado | 1 |

**Resumen LLM (gemma3:1b):**
La impresora térmica está funcionando correctamente, con la luz de error apagada y la luz de estado activa. Se confirma que el papel se está extrayendo correctamente y que el cabezal no presenta atascos.  Es importante verificar que la tapa esté cerrada y que los cables estén bien conectados (USB, Ethernet o Bluetooth).  Se recomienda revisar el cabezal para asegurar que la impresión está óptima.

## pinpad.md

| Término | Frecuencia |
|---|---:|
| pinpad | 2 |
| checklist | 1 |
| base | 1 |
| energía | 1 |
| batería | 1 |
| suficiente | 1 |
| cableado | 1 |
| firme | 1 |

**Resumen LLM (gemma3:1b):**
(Texto breve: se omite resumen LLM.)

## offline.md

| Término | Frecuencia |
|---|---:|
| pos | 7 |
| ventas | 4 |
| offline | 4 |
| modo | 2 |
| red | 2 |
| menú | 2 |
| registro | 2 |
| folio | 2 |

**Resumen LLM (gemma3:1b):**
El sistema POS indica "Offline" cuando la conexión de red falla. Se debe activar el modo offline en el POS (Menú → Modo Offline → Activar) y verificar visualmente la presencia del indicador "Offline".  Registrar cada venta como "pendiente" y conservar comprobantes/notas manuales.  Se limita a un máximo de N ventas offline por POS (configurable) y no se procesa devolución hasta la reanudación de la red.  Se debe escalar errores de sincronización con el ID POS y folio asociado.  Se debe evitar duplicados al sincronizar y seguir las políticas de los medios de pago.

## red_fisico.md

| Término | Frecuencia |
|---|---:|
| red | 2 |
| pos | 2 |
| switch | 2 |
| luz | 2 |
| checklist | 1 |
| físico | 1 |
| cable | 1 |
| insertado | 1 |

**Resumen LLM (gemma3:1b):**
**Resumen:**

Se requiere una verificación física de la red POS. El cable de red está correctamente insertado en el dispositivo POS y en el switch. Los LEDs del puerto del switch están encendidos (indicando actividad de Link/Activity). El router está encendido y la luz de Internet/WAN está activa.  Se debe verificar la presencia de un ONT/Modem si existe, y asegurar que la luz de LOS/Alarm está apagada.  También se debe descartar posibles problemas con adaptadores flojos o extensiones dañadas.  Verificar la conexión Wi-Fi: asegurar que el SSID es correcto y la intensidad de la señal sea suficiente.  Además, verificar la estabilidad de la energía, evitando saturación de las regletas.

## escaner_no_lee.md

| Término | Frecuencia |
|---|---:|
| código | 4 |
| sop | 1 |
| escáner | 1 |
| lee | 1 |
| pasos | 1 |
| limpiar | 1 |
| lente | 1 |
| verificar | 1 |

**Resumen LLM (gemma3:1b):**
El escáner no lee correctamente los códigos de barras. La solución implica limpiar la lente y verificar la iluminación. Se debe conectar el USB/revisar el cable. El escáner está configurado en modo HID. Se debe probar con códigos de prueba y, en caso de error, se debe realizar la entrada manual del código o buscarlo por nombre.  Se debe escalar el problema al modelo, serie y tipo de código.

## impresora_boleta.md

| Término | Frecuencia |
|---|---:|
| impresora | 16 |
| pos | 9 |
| tiempo | 7 |
| min | 7 |
| boletas | 6 |
| fiscal | 6 |
| estimado | 6 |
| procedimiento | 5 |

**Resumen LLM (gemma3:1b):**
La falla de la impresora de boletas en el terminal POS está causando problemas de continuidad operativa. Se requiere diagnosticar la causa raíz de la falla, que podría ser un fallo en la impresora o un problema de conexión. El procedimiento implica identificar al responsable de la falla (cajero/a o supervisor), y asegurar que se siga el procedimiento de resolución, incluyendo la verificación de la validación de la boleta.  La resolución debe priorizar la continuidad del proceso de caja y el cumplimiento de los requisitos legales de emisión de documentos tributarios.  Se recomienda verificar la causa de la falla y escalar a Nivel 2 si no se resuelve.

## impresora_no_imprime.md

| Término | Frecuencia |
|---|---:|
| impresora | 7 |
| impresión | 4 |
| pos | 4 |
| papel | 4 |
| ticket | 3 |
| tapa | 3 |
| imprime | 2 |
| min | 2 |

**Resumen LLM (gemma3:1b):**
La impresora no imprime, lo que indica un problema con la impresión.  Se observan errores de conexión, papel atascado, o luz de error.  Los pasos a seguir son: verificar el rollo térmico, cerrar la tapa, retirar el papel, revisar la conexión USB/Ethernet/Bluetooth, y luego imprimir un ticket de prueba.  Si la impresión falla, se debe marcar la venta como pendiente de impresión y reintentar la impresión cuando la impresora esté lista.  Se debe documentar la información relevante (modelo, serie, foto de luces/tapa/papel) en el archivo `docs/checklists/impresora_termica.md` y `docs/contingencia/offline.md`.

## pinpad_no_responde.md

| Término | Frecuencia |
|---|---:|
| pinpad | 4 |
| pasos | 2 |
| probar | 2 |
| sop | 1 |
| lector | 1 |
| tarjetas | 1 |
| responde | 1 |
| revisar | 1 |

**Resumen LLM (gemma3:1b):**
El pinpad/lector de tarjetas no responde.  Se debe verificar la energía/base y los cables. Reiniciar el pinpad (botón de encendido por 5 segundos).  Luego, realizar una prueba de transacción de $50 o probar el pinpad.  En caso de no responder, derivar a la caja vecina o utilizar un medio alternativo. Registrar el intento y el resultado.  Escalar el problema al equipo de soporte.

## red_caida.md

| Término | Frecuencia |
|---|---:|
| red | 10 |
| pos | 7 |
| tienda | 4 |
| probar | 3 |
| min | 3 |
| switch | 3 |
| reiniciar | 3 |
| offline | 3 |

**Resumen LLM (gemma3:1b):**
El sistema POS experimentó una caída de red, indicando un fallo de conectividad que requiere restablecimiento. Los indicadores muestran mensajes de "Sin conexión" o "Fallo de red". Los pasos inmediatos incluyen verificar el cable de red, reiniciar la conexión (router y switch), y probar la red con "Probar red". Si la prueba falla, activar el modo offline y registrar las ventas como pendientes de sincronización.  Se debe registrar el resultado de la prueba y la foto del router/switch para escalamiento y seguimiento.

## reinicio_pos.md

| Término | Frecuencia |
|---|---:|
| pos | 14 |
| aplicación | 9 |
| procedimiento | 6 |
| tiempo | 6 |
| caja | 6 |
| paso | 6 |
| reinicio | 5 |
| min | 5 |

**Resumen LLM (gemma3:1b):**
El procedimiento de reinicio de Terminal de Punto de Venta (POS) se establece para solucionar fallas de software, congelamiento o lentitud, minimizando el Tiempo de Recuperación (RTO) y garantizando la continuidad operativa en caja. Este procedimiento aplica a todos los terminales POS de las tiendas físicas y cubre a personal de caja y soporte de primera línea. Los responsables incluyen al cajero/a, el supervisor/a de tienda y la Mesa de Ayuda Nivel 1.  Se define un RTO de 10 minutos y un RPO de 5 minutos para la operación de POS.  Se requiere que el equipo no responda a los comandos de teclado, mouse o software.
