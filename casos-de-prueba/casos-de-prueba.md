# Casos de Prueba - Sistema de Gestión Bibliotecaria en GLPI
**Curso:** Pruebas de Software  
**Equipo:** Perez Huarachi Daniel | Palomino Sandoval Anderson | Sarmiento Castro Luis  
**Fecha de entrega:** 19/04/2026  
**Sistema bajo prueba:** GLPI v11.0.6 configurado como Sistema Bibliotecario  
**URL:** http://localhost:8080  
**Fecha de ejecución:** 12/04/2026

---

## Resumen de Ejecución

| Total | Pass | Fail | Bloqueado | N/A |
|-------|------|------|-----------|-----|
| 18 | 13 | 5 | 0 | 0 |

---

## TC-001: Registro exitoso de nuevo libro

| Campo | Valor |
|-------|-------|
| **ID** | TC-001 |
| **Módulo** | Gestión de Activos (Libros) |
| **Tipo** | Funcional - Positivo |
| **Prioridad** | Alta |
| **Ejecutado por** | Palomino Sandoval Anderson |
| **Fecha** | 12/04/2026 |

**Precondiciones:**
- Usuario autenticado con perfil Super-Admin
- Navegar a Activos > Computadoras

**Datos de entrada:**

| Campo GLPI | Valor de prueba |
|------------|-----------------|
| Nombre | Introducción a los Algoritmos |
| Número de serie | ISBN-9780262033848 |
| Nombre de usuario alternativo | Cormen, Thomas H. |
| Comentarios | MIT Press - 2009 - Tecnología |

**Pasos:**
1. Ir a Activos > Computadoras > + Añadir
2. Completar todos los campos según datos de entrada
3. Hacer clic en "+ Añadir"

**Resultado esperado:** El libro se crea correctamente. GLPI muestra mensaje de confirmación verde.

**Resultado obtenido:** El libro "Introducción a los Algoritmos" fue creado exitosamente con ID 14. GLPI mostró mensaje verde "Elemento añadido correctamente: Introducción a los Algoritmos".

**Evidencia:** `evidencias/TC-001-formulario.png` | `evidencias/TC-001-confirmacion.png`

**Estado: ✅ PASS**

---

## TC-002: Registro con campos obligatorios vacíos

| Campo | Valor |
|-------|-------|
| **ID** | TC-002 |
| **Módulo** | Gestión de Activos (Libros) |
| **Tipo** | Funcional - Negativo |
| **Prioridad** | Alta |
| **Ejecutado por** | Palomino Sandoval Anderson |
| **Fecha** | 12/04/2026 |

**Precondiciones:**
- Usuario autenticado con perfil Super-Admin
- Estar en el formulario de creación de activo

**Datos de entrada:**

| Campo | Valor |
|-------|-------|
| Nombre | (vacío) |
| Comentarios | Test campo vacío |

**Pasos:**
1. Ir a Activos > Computadoras > + Añadir
2. Dejar el campo "Nombre" vacío
3. Ingresar "Test campo vacío" en Comentarios
4. Hacer clic en "+ Añadir"

**Resultado esperado:** El sistema muestra mensaje de error indicando que el campo "Nombre" es obligatorio. El libro NO se crea.

**Resultado obtenido:** GLPI creó el elemento sin nombre (aparece como "N/A - ID 15"). No mostró ningún error ni validación. El campo Nombre NO es tratado como obligatorio.

**Evidencia:** `evidencias/TC-002-formulario-vacio.png` | `evidencias/TC-002-resultado.png`

**Estado: ❌ FAIL**

**Defecto encontrado:**
- **Bug ID:** BUG-001
- **Descripción:** El sistema permite registrar un libro sin nombre. No existe validación del campo obligatorio "Nombre". El activo queda registrado como "N/A".
- **Severidad:** Alta

---

## TC-003: Búsqueda de libro por título

| Campo | Valor |
|-------|-------|
| **ID** | TC-003 |
| **Módulo** | Gestión de Activos (Libros) |
| **Tipo** | Funcional - Positivo |
| **Prioridad** | Alta |
| **Ejecutado por** | Palomino Sandoval Anderson |
| **Fecha** | 12/04/2026 |

**Precondiciones:**
- 13 libros registrados en el sistema
- El libro "Cien años de soledad" existe

**Datos de entrada:**

| Campo | Valor |
|-------|-------|
| Búsqueda global | Cien |

**Pasos:**
1. Usar el buscador global de GLPI (barra superior)
2. Ingresar "Cien"
3. Presionar Enter

**Resultado esperado:** El sistema muestra "Cien años de soledad" en los resultados.

**Resultado obtenido:** La búsqueda "Cien" retornó "Cien años de soledad" con su ISBN correctamente. El sistema encontró el libro de forma inmediata.

**Evidencia:** `evidencias/TC-003-resultado.png`

**Estado: ✅ PASS**

---

## TC-004: Edición de datos de un libro

| Campo | Valor |
|-------|-------|
| **ID** | TC-004 |
| **Módulo** | Gestión de Activos (Libros) |
| **Tipo** | Funcional - Positivo |
| **Prioridad** | Media |
| **Ejecutado por** | Palomino Sandoval Anderson |
| **Fecha** | 12/04/2026 |

**Precondiciones:**
- El libro "Cien años de soledad" existe en el sistema

**Datos de entrada:**

| Campo | Valor original | Valor nuevo |
|-------|----------------|-------------|
| Comentarios | Sudamericana - 1967 - Literatura | Sudamericana - 1967 - Literatura - Edición revisada |

**Pasos:**
1. Buscar y abrir "Cien años de soledad"
2. Modificar el campo Comentarios
3. Hacer clic en "Guardar"

**Resultado esperado:** Los cambios se guardan correctamente con mensaje de confirmación.

**Resultado obtenido:** El comentario fue actualizado correctamente. GLPI mostró "Elemento modificado correctamente: Cien años de soledad". La fecha de última actualización cambió a 19:11.

**Evidencia:** `evidencias/TC-004-resultado.png`

**Estado: ✅ PASS**

---

## TC-005: Eliminación de libro (papelera)

| Campo | Valor |
|-------|-------|
| **ID** | TC-005 |
| **Módulo** | Gestión de Activos (Libros) |
| **Tipo** | Funcional - Positivo |
| **Prioridad** | Media |
| **Ejecutado por** | Palomino Sandoval Anderson |
| **Fecha** | 12/04/2026 |

**Precondiciones:**
- Existe el libro "Libro de prueba - ELIMINAR" en el sistema

**Pasos:**
1. Buscar y abrir "Libro de prueba - ELIMINAR"
2. Hacer clic en "Colocar en la papelera"
3. Confirmar la acción

**Resultado esperado:** El libro se mueve a la papelera. Ya no aparece en el listado principal.

**Resultado obtenido:** El libro "Libro de prueba - ELIMINAR" fue enviado a la papelera correctamente. GLPI mostró "Elemento borrado satisfactoriamente: Libro de prueba - ELIMINAR". Ya no aparece en el listado principal.

**Evidencia:** `evidencias/TC-005-resultado.png`

**Estado: ✅ PASS**

---

## TC-006: Creación de préstamo (ticket de solicitud)

| Campo | Valor |
|-------|-------|
| **ID** | TC-006 |
| **Módulo** | Gestión de Tickets (Préstamos) |
| **Tipo** | Funcional - Positivo |
| **Prioridad** | Alta |
| **Ejecutado por** | Palomino Sandoval Anderson |
| **Fecha** | 12/04/2026 |

**Precondiciones:**
- El libro "El señor de los anillos" existe en el sistema
- El usuario lector03 (Rosa Quispe) existe

**Datos de entrada:**

| Campo | Valor |
|-------|-------|
| Título | Préstamo: El señor de los anillos - Rosa Quispe |
| Descripción | Préstamo solicitado por Rosa Quispe. Devolución estimada: 2026-04-27 |
| Tipo | Solicitud |
| Categoría | Préstamo de libro |
| Solicitante | Quispe Rosa (lector03) |
| Elemento vinculado | El señor de los anillos (Computadora) |

**Pasos:**
1. Ir a Asistencia > Crear ticket
2. Completar todos los campos
3. Vincular el libro en la sección Elementos
4. Hacer clic en "+ Añadir"

**Resultado esperado:** El ticket de préstamo se crea con estado "En curso".

**Resultado obtenido:** Ticket #7 creado correctamente con tipo "Solicitud", categoría "Préstamo de libro", estado "En curso (asignada)", solicitante "Quispe Rosa" y libro "El señor de los anillos" vinculado.

**Evidencia:** `evidencias/TC-006-formulario.png` | `evidencias/TC-006-ticket-creado.png`

**Estado: ✅ PASS**

---

## TC-007: Préstamo de libro no disponible

| Campo | Valor |
|-------|-------|
| **ID** | TC-007 |
| **Módulo** | Gestión de Tickets (Préstamos) |
| **Tipo** | Funcional - Negativo |
| **Prioridad** | Alta |
| **Ejecutado por** | Palomino Sandoval Anderson |
| **Fecha** | 12/04/2026 |

**Precondiciones:**
- El libro "El señor de los anillos" tiene un ticket de préstamo activo (ticket #7)

**Pasos:**
1. Crear nuevo ticket de préstamo para "El señor de los anillos"
2. Asignarlo a lector02 (Carlos Torres)
3. Vincular el mismo libro
4. Guardar

**Resultado esperado:** El sistema advierte que el libro ya está prestado y no permite el segundo préstamo.

**Resultado obtenido:** GLPI creó el ticket #8 sin ningún error. Permitió prestar "El señor de los anillos" a Carlos Torres aunque ya estaba prestado a Rosa Quispe. No existe validación de disponibilidad.

**Evidencia:** `evidencias/TC-007-resultado.png`

**Estado: ❌ FAIL**

**Defecto encontrado:**
- **Bug ID:** BUG-002
- **Descripción:** El sistema permite crear múltiples tickets de préstamo para el mismo libro simultáneamente. No existe regla de negocio que verifique la disponibilidad del activo antes de crear un nuevo préstamo.
- **Severidad:** Alta

---

## TC-008: Devolución de libro (resolución de ticket)

| Campo | Valor |
|-------|-------|
| **ID** | TC-008 |
| **Módulo** | Gestión de Tickets (Préstamos) |
| **Tipo** | Funcional - Positivo |
| **Prioridad** | Alta |
| **Ejecutado por** | Palomino Sandoval Anderson |
| **Fecha** | 12/04/2026 |

**Precondiciones:**
- El ticket #7 (Préstamo: El señor de los anillos - Rosa Quispe) existe en estado "En curso"

**Pasos:**
1. Abrir el ticket #7
2. Agregar solución: "Libro devuelto en buen estado el 2026-04-12"
3. Cambiar estado a "Resuelto"
4. Aprobar la solución

**Resultado esperado:** El ticket queda en estado "Cerrado" con registro de fecha de resolución y cierre.

**Resultado obtenido:** El ticket #7 cambió a estado "Cerrado" con comentario "Libro devuelto en buen estado el 2026-04-12". Quedaron registradas fecha de resolución (19:25:17) y fecha de cierre (19:26:05).

**Evidencia:** `evidencias/TC-008-resultado.png`

**Estado: ✅ PASS**

---

## TC-009: Alerta de préstamo vencido

| Campo | Valor |
|-------|-------|
| **ID** | TC-009 |
| **Módulo** | Notificaciones / SLA |
| **Tipo** | Funcional - Positivo |
| **Prioridad** | Media |
| **Ejecutado por** | Palomino Sandoval Anderson |
| **Fecha** | 12/04/2026 |

**Precondiciones:**
- Existe el ticket #5 "Prestamo: El arte de la guerra - VENCIDO" con fecha de devolución 2026-03-20 (23 días vencido)

**Pasos:**
1. Abrir el ticket #5
2. Verificar si existe indicador visual de vencimiento
3. Verificar configuración de SLA y notificaciones

**Resultado esperado:** El sistema marca visualmente los tickets vencidos y genera alertas automáticas.

**Resultado obtenido:** El ticket aparece en estado "En curso (asignada)" sin ningún indicador visual de vencimiento (sin borde rojo, sin ícono de alerta). No existe SLA configurado para tickets de préstamo. No se generan alertas automáticas.

**Evidencia:** `evidencias/TC-009-ticket-vencido.png`

**Estado: ❌ FAIL**

**Defecto encontrado:**
- **Bug ID:** BUG-005
- **Descripción:** El sistema no genera alertas automáticas para préstamos vencidos. No existe indicador visual de vencimiento aunque el ticket tenga 23 días de mora. Requiere configuración manual de SLA que no está incluida en la instalación base.
- **Severidad:** Alta

---

## TC-010: Registro de nuevo usuario lector

| Campo | Valor |
|-------|-------|
| **ID** | TC-010 |
| **Módulo** | Gestión de Usuarios |
| **Tipo** | Funcional - Positivo |
| **Prioridad** | Alta |
| **Ejecutado por** | Palomino Sandoval Anderson |
| **Fecha** | 12/04/2026 |

**Precondiciones:**
- Usuario autenticado como Super-Admin
- El perfil "Lector" existe en el sistema

**Datos de entrada:**

| Campo | Valor |
|-------|-------|
| Login | lector06 |
| Apellido | Gutierrez |
| Nombre | Pedro |
| Perfil | Lector |
| Contraseña | Lector2024! |

**Pasos:**
1. Ir a Administración > Usuarios > + Añadir
2. Completar todos los campos
3. Guardar

**Resultado esperado:** El usuario se crea correctamente con perfil Lector.

**Resultado obtenido:** Usuario "lector06 - Gutierrez Pedro" creado correctamente con ID 14. GLPI mostró "Elemento añadido correctamente: Gutierrez Pedro".

**Evidencia:** `evidencias/TC-010-usuario-creado.png`

**Estado: ✅ PASS**

---

## TC-011: Intento de registro con DNI duplicado

| Campo | Valor |
|-------|-------|
| **ID** | TC-011 |
| **Módulo** | Gestión de Usuarios |
| **Tipo** | Funcional - Negativo |
| **Prioridad** | Alta |
| **Ejecutado por** | Palomino Sandoval Anderson |
| **Fecha** | 12/04/2026 |

**Precondiciones:**
- El usuario lector06 tiene Número Administrativo 72329114 registrado

**Datos de entrada:**

| Campo | Valor |
|-------|-------|
| Login | lector07 |
| Número Administrativo (DNI) | 72329114 (mismo que lector06) |

**Pasos:**
1. Crear nuevo usuario lector07
2. Ingresar el mismo Número Administrativo que lector06
3. Guardar

**Resultado esperado:** El sistema rechaza el registro e indica que el DNI ya está en uso.

**Resultado obtenido:** GLPI creó el usuario "Palomino Anderson" con el mismo Número Administrativo 72329114 sin ningún error ni advertencia. El sistema no valida unicidad del número de identificación.

**Evidencia:** `evidencias/TC-011-dni-duplicado.png`

**Estado: ❌ FAIL**

**Defecto encontrado:**
- **Bug ID:** BUG-003
- **Descripción:** El sistema permite registrar múltiples usuarios con el mismo número administrativo (DNI). No existe validación de unicidad para este campo. Dos usuarios distintos pueden tener el mismo identificador.
- **Severidad:** Alta

---

## TC-012: Login con credenciales inválidas

| Campo | Valor |
|-------|-------|
| **ID** | TC-012 |
| **Módulo** | Autenticación |
| **Tipo** | Funcional - Negativo / Seguridad |
| **Prioridad** | Alta |
| **Ejecutado por** | Palomino Sandoval Anderson |
| **Fecha** | 12/04/2026 |

**Precondiciones:**
- El usuario "lector01" existe en el sistema

**Datos de entrada:**

| Campo | Valor |
|-------|-------|
| Usuario | lector01 |
| Contraseña | contraseña_incorrecta |

**Pasos:**
1. Cerrar sesión
2. Ingresar usuario: lector01
3. Ingresar contraseña incorrecta
4. Hacer clic en "Iniciar sesión"

**Resultado esperado:** El sistema rechaza el login con mensaje genérico sin revelar si el usuario existe.

**Resultado obtenido:** El sistema rechazó el login y mostró mensaje genérico "Usuario o contraseña incorrecto". No reveló si el usuario existe o no. No permitió el acceso.

**Evidencia:** `evidencias/TC-012-login-fallido.png`

**Estado: ✅ PASS**

---

## TC-013: Verificación de permisos por rol

| Campo | Valor |
|-------|-------|
| **ID** | TC-013 |
| **Módulo** | Control de Acceso / Roles |
| **Tipo** | Funcional - Seguridad |
| **Prioridad** | Alta |
| **Ejecutado por** | Palomino Sandoval Anderson |
| **Fecha** | 12/04/2026 |

**Precondiciones:**
- El usuario lector01 existe con perfil "Lector" (Interfaz simplificada)

**Pasos:**
1. Autenticarse como lector01 / Lector2024!
2. Verificar menú disponible
3. Intentar acceder a http://localhost:8080/front/user.php (administración)

**Resultado esperado:** El usuario Lector solo ve portal simplificado. No puede acceder a módulos de administración.

**Resultado obtenido:** El usuario Lector solo vio el portal simplificado con opciones: Inicio, Service catalog, Casos. Al intentar acceder a /front/user.php, el sistema mostró "No tiene permisos para realizar esta acción". El control de acceso por rol funciona correctamente.

**Evidencia:** `evidencias/TC-013-acceso-lector.png` | `evidencias/TC-013-acceso-denegado.png`

**Estado: ✅ PASS**

---

## TC-014: Generación de reporte mensual de préstamos

| Campo | Valor |
|-------|-------|
| **ID** | TC-014 |
| **Módulo** | Reportes y Estadísticas |
| **Tipo** | Funcional - Positivo |
| **Prioridad** | Media |
| **Ejecutado por** | Palomino Sandoval Anderson |
| **Fecha** | 12/04/2026 |

**Precondiciones:**
- Existen tickets de préstamo creados en el sistema

**Pasos:**
1. Ir a Asistencia > Estadísticas
2. Seleccionar "Tiquetes - Global"
3. Período: 2025-04-12 a 2026-04-12
4. Hacer clic en "Mostrar reporte"

**Resultado esperado:** El sistema muestra reporte con gráficos de tickets del período.

**Resultado obtenido:** GLPI generó el reporte "Tiquetes - Global" con gráficos de: Número de casos (Opened/Solved/Tarde/Cerrado), Tiempo promedio en horas (cierre/resolución/duración real), Encuesta de satisfacción. Se visualiza el pico de tickets creados en abril 2026 correspondiente a los préstamos registrados durante las pruebas.

**Evidencia:** `evidencias/TC-014-reporte.png`

**Estado: ✅ PASS**

---

## TC-015: Exportación de reporte a PDF/CSV

| Campo | Valor |
|-------|-------|
| **ID** | TC-015 |
| **Módulo** | Reportes y Estadísticas |
| **Tipo** | Funcional - Positivo |
| **Prioridad** | Media |
| **Ejecutado por** | Palomino Sandoval Anderson |
| **Fecha** | 12/04/2026 |

**Precondiciones:**
- Estar en el listado de Activos > Computadoras

**Pasos:**
1. Ir a Activos > Computadoras
2. Hacer clic en el ícono de descarga (↓) arriba a la derecha
3. Seleccionar formato CSV
4. Verificar descarga

**Resultado esperado:** El archivo se descarga correctamente en el formato seleccionado.

**Resultado obtenido:** El archivo "glpi.csv" se descargó correctamente. GLPI ofrece exportación en múltiples formatos: Landscape PDF, Portrait PDF, CSV, Spreadsheet (ODS) y Spreadsheet (XLSX), tanto para la página actual como para todas las páginas.

**Evidencia:** `evidencias/TC-015-opciones-export.png` | `evidencias/TC-015-csv-descargado.png`

**Estado: ✅ PASS**

---

## TC-016: Filtrado de libros por categoría

| Campo | Valor |
|-------|-------|
| **ID** | TC-016 |
| **Módulo** | Gestión de Activos / Búsqueda |
| **Tipo** | Funcional - Positivo |
| **Prioridad** | Media |
| **Ejecutado por** | Palomino Sandoval Anderson |
| **Fecha** | 12/04/2026 |

**Precondiciones:**
- 4 libros de categoría "Tecnología" existen en el sistema

**Pasos:**
1. Ir a Activos > Computadoras
2. Abrir búsqueda avanzada
3. Criterio: Comentarios > contiene > "Tecnologia"
4. Hacer clic en Buscar

**Resultado esperado:** Solo aparecen libros de la categoría Tecnología.

**Resultado obtenido:** El filtro devolvió exactamente 4 libros: Clean Code, The Pragmatic Programmer, Fundamentos de programacion, Introducción a los Algoritmos. Todos con comentario que incluye "Tecnologia". El listado muestra "Mostrando filas 1-4 de 4".

**Evidencia:** `evidencias/TC-016-filtro-tecnologia.png`

**Estado: ✅ PASS**

---

## TC-017: Tiempo de respuesta en búsqueda

| Campo | Valor |
|-------|-------|
| **ID** | TC-017 |
| **Módulo** | Rendimiento |
| **Tipo** | No funcional - Rendimiento |
| **Prioridad** | Baja |
| **Ejecutado por** | Palomino Sandoval Anderson |
| **Fecha** | 12/04/2026 |

**Criterio de aceptación:** Tiempo de carga < 3000 ms en red local.

**Pasos:**
1. Abrir DevTools (F12) > Network
2. Navegar a Activos > Computadoras
3. Medir tiempos de respuesta

**Resultado obtenido:**

| Operación | Tiempo medido |
|-----------|---------------|
| Waiting for server response | 4.15 ms |
| Content Download | 9.56 ms |
| Total request | 18.40 ms |

**Resultado:** Muy por debajo del criterio de aceptación de 3000 ms. El sistema responde en menos de 20ms en red local con Docker.

**Evidencia:** `evidencias/TC-017-devtools-network.png`

**Estado: ✅ PASS**

---

## TC-018: Sincronización préstamo-inventario

| Campo | Valor |
|-------|-------|
| **ID** | TC-018 |
| **Módulo** | Integración Tickets-Activos |
| **Tipo** | Funcional - Integración |
| **Prioridad** | Alta |
| **Ejecutado por** | Palomino Sandoval Anderson |
| **Fecha** | 12/04/2026 |

**Precondiciones:**
- El libro "Clean Code" existe con ticket de préstamo activo (#1)

**Pasos:**
1. Verificar estado del libro "Clean Code" en Activos
2. Verificar que tiene ticket de préstamo activo vinculado
3. Comprobar si el estado cambió automáticamente

**Resultado esperado:** El estado del libro cambia automáticamente al crear un ticket de préstamo.

**Resultado obtenido:** El estado del libro "Clean Code" no cambió al tener un ticket de préstamo activo vinculado. El sistema NO sincroniza automáticamente el estado del inventario con los tickets. El bibliotecario debe cambiar el estado manualmente.

**Evidencia:** `evidencias/TC-018-estado-libro.png` | `evidencias/TC-018-ticket-activo.png`

**Estado: ❌ FAIL**

**Defecto encontrado:**
- **Bug ID:** BUG-004
- **Descripción:** El sistema no actualiza automáticamente el estado del activo (libro) al crear o resolver un ticket de préstamo. El cambio de estado requiere intervención manual del bibliotecario, lo que puede generar inconsistencias en el inventario.
- **Severidad:** Alta

---

## Registro de Defectos Encontrados

| Bug ID | TC | Descripción | Severidad | Estado |
|--------|-----|-------------|-----------|--------|
| BUG-001 | TC-002 | Campo "Nombre" no es validado como obligatorio. El sistema crea activos sin nombre (N/A). | Alta | Abierto |
| BUG-002 | TC-007 | Sistema permite préstamo de libro ya prestado. No valida disponibilidad del activo. | Alta | Abierto |
| BUG-003 | TC-011 | No valida unicidad del Número Administrativo (DNI). Permite duplicados. | Alta | Abierto |
| BUG-004 | TC-018 | Estado del inventario no se sincroniza automáticamente con tickets de préstamo. | Alta | Abierto |
| BUG-005 | TC-009 | No genera alertas automáticas para préstamos vencidos. Sin indicador visual de mora. | Alta | Abierto |

---

## Configuración de GLPI para Pruebas

**Versión GLPI:** 11.0.6  
**URL:** http://localhost:8080  
**Infraestructura:** Docker Compose (diouxx/glpi + mysql:8.0)

**Credenciales de prueba:**

| Rol | Usuario | Contraseña |
|-----|---------|------------|
| Admin | glpi | glpi |
| Bibliotecario | biblio01 | Biblio2024! |
| Bibliotecario | biblio02 | Biblio2024! |
| Lector | lector01 | Lector2024! |
| Lector | lector02 | Lector2024! |
| Lector | lector03 | Lector2024! |
| Lector | lector04 | Lector2024! |
| Lector | lector05 | Lector2024! |
| Lector | lector06 | Lector2024! |

---

## Conclusiones

De los 18 casos de prueba ejecutados:
- **13 casos PASS (72%):** Las funcionalidades básicas de gestión de activos, búsqueda, autenticación, control de acceso, reportes y exportación funcionan correctamente.
- **5 casos FAIL (28%):** Se identificaron limitaciones propias de GLPI como sistema de gestión de TI adaptado para uso bibliotecario.

Los 5 defectos encontrados (BUG-001 al BUG-005) son limitaciones inherentes de GLPI al ser usado fuera de su propósito original. Un sistema bibliotecario dedicado requeriría validaciones específicas del dominio como: campo nombre obligatorio, control de disponibilidad de ejemplares, unicidad de DNI, sincronización automática de inventario y alertas de mora configuradas por defecto.
