# Guía de Instalación y Configuración — GLPI Biblioteca
**Equipo:** Perez Huarachi Daniel | Palomino Sandoval Anderson | Sarmiento Castro Luis  
**Entrega:** 19/04/2026

---

## Fase 1: Levantar GLPI con Docker

### Requisitos previos
- Docker Desktop instalado y corriendo
- Puerto 8080 libre

### Pasos

```bash
# 1. Ir a la carpeta del proyecto
cd "C:\Users\ander\OneDrive\Documentos\GLPI-Biblioteca"

# 2. Levantar los contenedores
docker compose up -d

# 3. Verificar que estén corriendo
docker ps
```

Esperar ~30-60 segundos. Luego abrir: **http://localhost:8080**

> Si 8080 está ocupado, editar docker-compose.yml y cambiar "8080:80" por "8181:80"

---

## Fase 2: Instalador web de GLPI

Al abrir http://localhost:8080 se mostrará el wizard de instalación.

### Paso 1 — Idioma
- Seleccionar: **Español**
- Siguiente

### Paso 2 — Licencia
- Aceptar términos → Siguiente

### Paso 3 — Comprobación de prerequisitos
- Todo debe aparecer en verde ✓
- Si hay warnings de PHP, ignorar (no afectan funcionalidad básica)
- Siguiente

### Paso 4 — Conexión a base de datos
| Campo | Valor |
|-------|-------|
| Servidor SQL | `mysql` (nombre del contenedor) |
| Usuario SQL | `glpi` |
| Contraseña SQL | `glpi123` |

- Conectar → Seleccionar base de datos: **glpi** → Siguiente

### Paso 5 — Inicializar base de datos
- Hacer clic en "Continuar" → esperar ~1-2 minutos

### Paso 6 — Configuración de la instancia
- Nombre: **Sistema Bibliotecario - Vida Divina**
- Email admin: andersonpalominosandoval@gmail.com
- Siguiente → Finalizar

### Credenciales por defecto
| Usuario | Contraseña |
|---------|------------|
| glpi | glpi |
| tech | tech |
| normal | normal |
| post-only | postonly |

**Importante:** Cambiar contraseña de glpi en primer login.

---

## Fase 3: Configuración inicial de GLPI

### 3.1 Idioma y zona horaria
1. Setup > Configuración general
2. Idioma: Español
3. Zona horaria: America/Lima (UTC-5)
4. Guardar

### 3.2 Habilitar API REST (para script de carga de datos)
1. Setup > Configuración general > pestaña **API**
2. Habilitar API REST: **Sí**
3. Habilitar login con credenciales: **Sí**
4. Generar App Token → copiar el valor
5. Guardar

### 3.3 Configurar nombre de la instancia
1. Setup > Configuración general > pestaña **General**
2. Nombre del helpdesk: **Biblioteca - Sistema de Gestión**
3. URL: http://localhost:8080
4. Guardar

---

## Fase 4: Crear perfil "Lector"

1. Administración > Perfiles > + Agregar
2. Nombre: **Lector**
3. Configurar permisos:
   - **Herramientas > Crear ticket: Sí**
   - **Herramientas > Ver mis tickets: Sí**
   - Todo lo demás: **No**
4. Guardar

---

## Fase 5: Crear categorías de libros

Las categorías se configuran en **Configuración > Listas desplegables > Categorías de ITIL**.

1. Asistencia > Configuración > Categorías de tickets > + Agregar
2. Crear cada una:

| Nombre | Descripción |
|--------|-------------|
| Literatura | Novelas, cuentos, poesía |
| Ciencias | Física, Química, Biología, Matemáticas |
| Historia | Historia universal, peruana, geografía |
| Tecnología | Informática, ingeniería, programación |
| Arte | Pintura, música, arquitectura, diseño |
| Préstamo de libro | Categoría para tickets de préstamo |

---

## Fase 6: Configurar estados de activos (para libros)

1. Configuración > Listas desplegables > Estados de los ítems
2. Verificar que existan:
   - **En stock** → se usará como "Disponible"
   - **En reparación** → se usará como "Prestado"
   - **Reciclado** → se usará como "Vencido/Baja"
3. Si no existen, crearlos con esos nombres

---

## Fase 7: Crear tipo "Libro"

1. Activos > Configuración > Tipos de computadoras > + Agregar
2. Nombre: **Libro**
3. Comentario: Tipo de activo para libros de la biblioteca
4. Guardar

---

## Fase 8: Registrar los libros

Ir a **Activos > Computadoras > + Agregar** y registrar cada libro:

> **Convención de campos:**
> - **Nombre** = Título del libro
> - **Número de serie** = ISBN
> - **Número de inventario** = Autor
> - **Comentarios** = Editorial | Año | Categoría
> - **Tipo** = Libro
> - **Estado** = En stock (Disponible)

### Lista de libros a registrar:

| # | Título | ISBN | Autor | Editorial/Año/Cat |
|---|--------|------|-------|-------------------|
| 1 | Cien años de soledad | ISBN-9780307474728 | García Márquez, Gabriel | Sudamericana\|1967\|Literatura |
| 2 | El señor de los anillos | ISBN-9780618640157 | Tolkien, J.R.R. | Minotauro\|1954\|Literatura |
| 3 | Breve historia del tiempo | ISBN-9780553380163 | Hawking, Stephen | Crítica\|1988\|Ciencias |
| 4 | El gen egoísta | ISBN-9780198788607 | Dawkins, Richard | Salvat\|1976\|Ciencias |
| 5 | Sapiens: De animales a dioses | ISBN-9788499926223 | Harari, Yuval Noah | Debate\|2011\|Historia |
| 6 | El arte de la guerra | ISBN-9788441413153 | Sun Tzu | Edaf\|Siglo V aC\|Historia |
| 7 | Clean Code | ISBN-9780132350884 | Martin, Robert C. | Prentice Hall\|2008\|Tecnología |
| 8 | The Pragmatic Programmer | ISBN-9780201616224 | Hunt, Andrew | Addison-Wesley\|1999\|Tecnología |
| 9 | El arte | ISBN-9788449305993 | Read, Herbert | Omega\|1931\|Arte |
| 10 | Fundamentos de programación | ISBN-9786073238403 | Joyanes, Luis | McGraw-Hill\|2008\|Tecnología |
| 11 | Historia del Perú | ISBN-9789972217234 | Basadre, Jorge | El Comercio\|2005\|Historia |
| 12 | Química general | ISBN-9786071505088 | Chang, Raymond | McGraw-Hill\|2010\|Ciencias |
| 13 | Libro de prueba - ELIMINAR | ISBN-0000000001 | Autor Test | Test\|2024\|Test |

---

## Fase 9: Crear usuarios

### 9.1 Usuarios Lectores
Ir a **Administración > Usuarios > + Agregar**

| Login | Nombre | Apellido | Email | Perfil |
|-------|--------|----------|-------|--------|
| lector01 | María | Flores | maria.flores@biblioteca.pe | Lector (Self-Service) |
| lector02 | Carlos | Torres | carlos.torres@biblioteca.pe | Lector (Self-Service) |
| lector03 | Rosa | Quispe | rosa.quispe@biblioteca.pe | Lector (Self-Service) |
| lector04 | Juan | Mendoza | juan.mendoza@biblioteca.pe | Lector (Self-Service) |
| lector05 | Elena | Vargas | elena.vargas@biblioteca.pe | Lector (Self-Service) |

Contraseña para todos: **Lector2024!**

### 9.2 Usuarios Bibliotecarios

| Login | Nombre | Apellido | Email | Perfil |
|-------|--------|----------|-------|--------|
| biblio01 | Daniel | Pérez | daniel.perez@biblioteca.pe | Técnico (Technician) |
| biblio02 | Luis | Sarmiento | luis.sarmiento@biblioteca.pe | Técnico (Technician) |

Contraseña para ambos: **Biblio2024!**

---

## Fase 10: Crear préstamos de ejemplo (tickets)

Ir a **Asistencia > Tickets > + Crear** y registrar:

| # | Título ticket | Solicitante | Libro vinculado | Estado |
|---|--------------|-------------|-----------------|--------|
| 1 | Préstamo: Clean Code - María Flores | lector01 | Clean Code | En curso |
| 2 | Préstamo: Sapiens - Carlos Torres | lector02 | Sapiens | En curso |
| 3 | Préstamo: Cien años - Rosa Quispe | lector03 | Cien años de soledad | Resuelto |
| 4 | Préstamo: Historia del Perú - Juan Mendoza | lector04 | Historia del Perú | En curso |
| 5 | Préstamo: El gen egoísta - Elena Vargas | lector05 | El gen egoísta | Resuelto |
| 6 | Préstamo: Arte de la guerra - lector01 | lector01 | El arte de la guerra | En curso (vencido) |

Para tickets "Resueltos": agregar solución "Libro devuelto" y cambiar estado.
Para ticket vencido: editar fecha de apertura para que sea > 15 días atrás.

---

## Fase 11: Configurar SLA para préstamos

1. Asistencia > Configuración > SLA > + Agregar
2. Nombre: **SLA Préstamo 15 días**
3. Tipo: Tiempo de resolución
4. Tiempo máximo: 15 días
5. Calendario: 24/7 o Horario biblioteca
6. Guardar
7. Aplicar a categoría "Préstamo de libro" via reglas de negocio

---

## Verificación final

Antes de ejecutar casos de prueba, verificar:

- [ ] GLPI accesible en http://localhost:8080
- [ ] 13 libros registrados (incluido el de prueba)
- [ ] 5 lectores creados
- [ ] 2 bibliotecarios creados
- [ ] 6 tickets de préstamo creados
- [ ] Categorías de tickets creadas
- [ ] SLA configurado

---

## Comandos útiles

```bash
# Ver logs de GLPI
docker logs glpi -f

# Ver logs de MySQL
docker logs glpi-mysql -f

# Reiniciar servicios
docker compose restart

# Detener todo
docker compose down

# Detener y eliminar datos (CUIDADO: borra todo)
docker compose down -v

# Entrar al contenedor GLPI
docker exec -it glpi bash

# Ejecutar SQL directamente
docker exec -it glpi-mysql mysql -u glpi -pglpi123 glpi
```

---

## Solución de problemas comunes

### GLPI muestra error de base de datos
```bash
# Verificar que MySQL esté corriendo
docker ps | grep mysql

# Ver logs de MySQL
docker logs glpi-mysql

# El contenedor GLPI puede necesitar más tiempo para conectar
docker compose restart glpi
```

### Puerto 8080 ocupado
```bash
# Windows: ver qué usa el puerto
netstat -ano | findstr :8080

# Cambiar puerto en docker-compose.yml: "8181:80"
```

### La instalación web no avanza
- Limpiar caché del navegador (Ctrl+Shift+R)
- Intentar en modo incógnito
- Revisar `docker logs glpi`

### Reiniciar instalación desde cero
```bash
docker compose down -v
docker compose up -d
# Esperar 60 segundos y volver a http://localhost:8080
```
