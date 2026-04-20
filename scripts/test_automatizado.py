"""
Pruebas Automatizadas - Sistema Bibliotecario GLPI
Equipo: Perez Huarachi Daniel | Palomino Sandoval Anderson | Sarmiento Castro Luis
Curso: Pruebas de Software - UTP
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8080/apirest.php"
APP_TOKEN = "QeoDpRHCafYbpLJQb15IjZIyUQyNyccuxR97X3r1"
USER = "glpi"
PASSWORD = "glpi"

resultados = []
libro_prueba_id = None
ticket_prueba_id = None

def log(tc_id, nombre, estado, detalle=""):
    icon = "[PASS]" if estado == "PASS" else "[FAIL]"
    print(f"  {icon} | {tc_id} - {nombre}")
    if detalle:
        print(f"         {detalle}")
    resultados.append({
        "id": tc_id,
        "nombre": nombre,
        "estado": estado,
        "detalle": detalle
    })

def iniciar_sesion(user=USER, password=PASSWORD):
    resp = requests.get(
        f"{BASE_URL}/initSession",
        headers={"App-Token": APP_TOKEN},
        auth=(user, password)
    )
    if resp.status_code == 200:
        return resp.json()["session_token"]
    return None

def cerrar_sesion(token):
    requests.get(
        f"{BASE_URL}/killSession",
        headers={"App-Token": APP_TOKEN, "Session-Token": token}
    )

def h(token):
    return {"App-Token": APP_TOKEN, "Session-Token": token, "Content-Type": "application/json"}

# ── TC-AUTO-01: Registro de libro (TC-001) ───────────────────────────────────
def tc_auto_01(token):
    global libro_prueba_id
    payload = {"input": {
        "name": "Libro de Prueba Automatizada",
        "serial": "ISBN-AUTO-TEST-001",
        "comment": "Creado por script de pruebas automatizadas - UTP"
    }}
    resp = requests.post(f"{BASE_URL}/Computer", headers=h(token), json=payload)
    if resp.status_code == 201:
        libro_prueba_id = resp.json()["id"]
        log("TC-AUTO-01", "Registro de nuevo libro en el catalogo", "PASS",
            f"Libro creado con ID: {libro_prueba_id}")
    else:
        log("TC-AUTO-01", "Registro de nuevo libro en el catalogo", "FAIL",
            f"HTTP {resp.status_code}: {resp.text[:80]}")

# ── TC-AUTO-02: Busqueda de libro por nombre (TC-002) ────────────────────────
def tc_auto_02(token):
    resp = requests.get(
        f"{BASE_URL}/Computer",
        headers=h(token),
        params={"searchText[name]": "Clean Code", "range": "0-10"}
    )
    if resp.status_code == 200:
        libros = resp.json()
        if isinstance(libros, list) and len(libros) > 0:
            log("TC-AUTO-02", "Busqueda de libro por nombre", "PASS",
                f"Se encontraron {len(libros)} resultado(s) para 'Clean Code'")
        else:
            log("TC-AUTO-02", "Busqueda de libro por nombre", "FAIL",
                "No se encontraron resultados para 'Clean Code'")
    else:
        log("TC-AUTO-02", "Busqueda de libro por nombre", "FAIL", f"HTTP {resp.status_code}")

# ── TC-AUTO-03: Editar informacion de libro (TC-003) ─────────────────────────
def tc_auto_03(token):
    if not libro_prueba_id:
        log("TC-AUTO-03", "Edicion de datos de libro", "FAIL", "No hay libro de prueba disponible")
        return
    payload = {"input": {"name": "Libro de Prueba Automatizada - EDITADO"}}
    resp = requests.put(f"{BASE_URL}/Computer/{libro_prueba_id}", headers=h(token), json=payload)
    if resp.status_code == 200:
        log("TC-AUTO-03", "Edicion de datos de libro", "PASS",
            f"Libro ID {libro_prueba_id} actualizado correctamente")
    else:
        log("TC-AUTO-03", "Edicion de datos de libro", "FAIL", f"HTTP {resp.status_code}")

# ── TC-AUTO-04: Listar catalogo completo (TC-004) ────────────────────────────
def tc_auto_04(token):
    resp = requests.get(f"{BASE_URL}/Computer", headers=h(token), params={"range": "0-100"})
    if resp.status_code == 200:
        libros = resp.json()
        total = len(libros)
        if total >= 12:
            log("TC-AUTO-04", "Visualizacion del catalogo completo de libros", "PASS",
                f"Catalogo accesible con {total} activos registrados")
        else:
            log("TC-AUTO-04", "Visualizacion del catalogo completo de libros", "FAIL",
                f"Solo {total} activos (se esperaban >= 12)")
    else:
        log("TC-AUTO-04", "Visualizacion del catalogo completo de libros", "FAIL", f"HTTP {resp.status_code}")

# ── TC-AUTO-05: Verificar estado de libro (TC-005) ───────────────────────────
def tc_auto_05(token):
    resp = requests.get(f"{BASE_URL}/Computer", headers=h(token),
                        params={"searchText[name]": "Clean Code"})
    if resp.status_code == 200 and resp.json():
        libro = resp.json()[0]
        estado_id = libro.get("states_id", None)
        log("TC-AUTO-05", "Verificacion de estado de libro en inventario", "PASS",
            f"Libro 'Clean Code' encontrado, estado_id={estado_id}")
    else:
        log("TC-AUTO-05", "Verificacion de estado de libro en inventario", "FAIL",
            "No se pudo obtener el libro o su estado")

# ── TC-AUTO-06: Crear ticket de prestamo (TC-006) ────────────────────────────
def tc_auto_06(token):
    global ticket_prueba_id
    payload = {"input": {
        "name": "Prestamo Automatizado - Test UTP",
        "content": "Solicitud de prestamo generada por prueba automatizada",
        "status": 1,
        "type": 1,
        "itilcategories_id": 0
    }}
    resp = requests.post(f"{BASE_URL}/Ticket", headers=h(token), json=payload)
    if resp.status_code == 201:
        ticket_prueba_id = resp.json()["id"]
        log("TC-AUTO-06", "Creacion de ticket de prestamo", "PASS",
            f"Ticket creado con ID: {ticket_prueba_id}")
    else:
        log("TC-AUTO-06", "Creacion de ticket de prestamo", "FAIL",
            f"HTTP {resp.status_code}: {resp.text[:80]}")

# ── TC-AUTO-07: Prestamo duplicado - BUG-002 (TC-007) ────────────────────────
def tc_auto_07(token):
    payload = {"input": {
        "name": "Prestamo Duplicado BUG-002",
        "content": "Test automatico de prestamo duplicado",
        "status": 1, "type": 1
    }}
    resp1 = requests.post(f"{BASE_URL}/Ticket", headers=h(token), json=payload)
    resp2 = requests.post(f"{BASE_URL}/Ticket", headers=h(token), json=payload)
    if resp1.status_code == 201 and resp2.status_code == 201:
        id1, id2 = resp1.json()["id"], resp2.json()["id"]
        log("TC-AUTO-07", "Validacion prestamo duplicado (BUG-002)", "FAIL",
            f"BUG confirmado: GLPI acepto dos tickets identicos (ID {id1} e ID {id2}). Sin validacion de duplicados.")
        requests.delete(f"{BASE_URL}/Ticket/{id1}", headers=h(token))
        requests.delete(f"{BASE_URL}/Ticket/{id2}", headers=h(token))
    else:
        log("TC-AUTO-07", "Validacion prestamo duplicado (BUG-002)", "PASS",
            "Sistema rechazo correctamente el prestamo duplicado")

# ── TC-AUTO-08: Cambio de estado de ticket (devolucion) (TC-008) ─────────────
def tc_auto_08(token):
    if not ticket_prueba_id:
        log("TC-AUTO-08", "Devolucion de libro (cambio estado ticket)", "FAIL",
            "No hay ticket de prueba disponible")
        return
    payload = {"input": {"status": 5}}  # 5 = Resuelto en GLPI
    resp = requests.put(f"{BASE_URL}/Ticket/{ticket_prueba_id}", headers=h(token), json=payload)
    if resp.status_code == 200:
        log("TC-AUTO-08", "Devolucion de libro (cambio estado ticket a Resuelto)", "PASS",
            f"Ticket ID {ticket_prueba_id} marcado como Resuelto")
    else:
        log("TC-AUTO-08", "Devolucion de libro (cambio estado ticket a Resuelto)", "FAIL",
            f"HTTP {resp.status_code}")

# ── TC-AUTO-09: Creacion de usuario (TC-009) ─────────────────────────────────
def tc_auto_09(token):
    payload = {"input": {
        "name": "lector_auto_test",
        "realname": "Test Automatizado",
        "firstname": "Lector",
        "password": "Test2024!",
        "password2": "Test2024!"
    }}
    resp = requests.post(f"{BASE_URL}/User", headers=h(token), json=payload)
    if resp.status_code == 201:
        user_id = resp.json()["id"]
        log("TC-AUTO-09", "Creacion de nuevo usuario lector", "PASS",
            f"Usuario creado con ID: {user_id}")
        requests.delete(f"{BASE_URL}/User/{user_id}", headers=h(token))
    else:
        log("TC-AUTO-09", "Creacion de nuevo usuario lector", "FAIL",
            f"HTTP {resp.status_code}: {resp.text[:80]}")

# ── TC-AUTO-10: Autenticacion con credenciales invalidas (TC-010) ─────────────
def tc_auto_10():
    resp = requests.get(
        f"{BASE_URL}/initSession",
        headers={"App-Token": APP_TOKEN},
        auth=("glpi", "password_incorrecta_123")
    )
    if resp.status_code in [400, 401]:
        log("TC-AUTO-10", "Autenticacion con credenciales invalidas", "PASS",
            f"Sistema rechazo correctamente (HTTP {resp.status_code})")
    else:
        log("TC-AUTO-10", "Autenticacion con credenciales invalidas", "FAIL",
            f"Sistema acepto credenciales invalidas (HTTP {resp.status_code})")

# ── TC-AUTO-11: Autenticacion valida (TC-011) ────────────────────────────────
def tc_auto_11():
    token = iniciar_sesion()
    if token and len(token) > 10:
        log("TC-AUTO-11", "Autenticacion con credenciales validas", "PASS",
            f"Session token obtenido: {token[:20]}...")
        cerrar_sesion(token)
    else:
        log("TC-AUTO-11", "Autenticacion con credenciales validas", "FAIL",
            "No se obtuvo session token valido")

# ── TC-AUTO-12: Verificar perfil del usuario autenticado (TC-012) ─────────────
def tc_auto_12(token):
    resp = requests.get(f"{BASE_URL}/getMyProfiles", headers=h(token))
    if resp.status_code == 200:
        perfiles = resp.json().get("myprofiles", [])
        if perfiles:
            nombres = [p.get("name", "?") for p in perfiles]
            log("TC-AUTO-12", "Verificacion de perfil del usuario autenticado", "PASS",
                f"Perfiles asignados: {', '.join(nombres)}")
        else:
            log("TC-AUTO-12", "Verificacion de perfil del usuario autenticado", "FAIL",
                "Usuario sin perfiles asignados")
    else:
        log("TC-AUTO-12", "Verificacion de perfil del usuario autenticado", "FAIL",
            f"HTTP {resp.status_code}")

# ── TC-AUTO-13: Verificar SLA en tickets (TC-013) ────────────────────────────
def tc_auto_13(token):
    resp = requests.get(f"{BASE_URL}/Ticket", headers=h(token), params={"range": "0-10"})
    if resp.status_code == 200:
        tickets = resp.json()
        if tickets:
            t = tickets[0]
            tiene_sla = "time_to_resolve" in t or "slas_id_ttr" in t
            if tiene_sla:
                log("TC-AUTO-13", "Verificacion de SLA en tickets de prestamo", "PASS",
                    "Campo de SLA presente en estructura de tickets")
            else:
                log("TC-AUTO-13", "Verificacion de SLA en tickets de prestamo", "FAIL",
                    "Campo SLA no encontrado en tickets")
        else:
            log("TC-AUTO-13", "Verificacion de SLA en tickets de prestamo", "FAIL",
                "No hay tickets para verificar")
    else:
        log("TC-AUTO-13", "Verificacion de SLA en tickets de prestamo", "FAIL",
            f"HTTP {resp.status_code}")

# ── TC-AUTO-14: Acceso a reportes via API (TC-014) ───────────────────────────
def tc_auto_14(token):
    resp = requests.get(f"{BASE_URL}/Ticket", headers=h(token), params={"range": "0-100"})
    if resp.status_code == 200:
        tickets = resp.json()
        resueltos = sum(1 for t in tickets if t.get("status") == 5)
        abiertos = sum(1 for t in tickets if t.get("status") in [1, 2])
        log("TC-AUTO-14", "Generacion de reporte de prestamos", "PASS",
            f"Total tickets: {len(tickets)} | Resueltos: {resueltos} | Abiertos: {abiertos}")
    else:
        log("TC-AUTO-14", "Generacion de reporte de prestamos", "FAIL", f"HTTP {resp.status_code}")

# ── TC-AUTO-15: Exportacion de datos (TC-015) ────────────────────────────────
def tc_auto_15(token):
    resp = requests.get(
        f"{BASE_URL}/Computer",
        headers={**h(token), "Accept": "application/json"},
        params={"range": "0-50"}
    )
    if resp.status_code == 200 and resp.headers.get("Content-Type", "").startswith("application/json"):
        data = resp.json()
        log("TC-AUTO-15", "Exportacion de datos del catalogo en JSON", "PASS",
            f"Datos exportados correctamente: {len(data)} registros en formato JSON")
    else:
        log("TC-AUTO-15", "Exportacion de datos del catalogo en JSON", "FAIL",
            f"HTTP {resp.status_code}")

# ── TC-AUTO-16: Busqueda avanzada con filtros (TC-016) ───────────────────────
def tc_auto_16(token):
    resp = requests.get(
        f"{BASE_URL}/Computer",
        headers=h(token),
        params={"searchText[comment]": "Tecnologia", "range": "0-20"}
    )
    if resp.status_code == 200:
        resultados_busqueda = resp.json()
        log("TC-AUTO-16", "Busqueda avanzada por categoria Tecnologia", "PASS",
            f"Busqueda ejecutada correctamente, {len(resultados_busqueda)} resultado(s)")
    else:
        log("TC-AUTO-16", "Busqueda avanzada por categoria Tecnologia", "FAIL",
            f"HTTP {resp.status_code}")

# ── TC-AUTO-17: Tiempo de respuesta del sistema (TC-017) ─────────────────────
def tc_auto_17(token):
    inicio = time.time()
    resp = requests.get(f"{BASE_URL}/Computer", headers=h(token), params={"range": "0-50"})
    duracion = (time.time() - inicio) * 1000
    if resp.status_code == 200 and duracion < 3000:
        log("TC-AUTO-17", "Tiempo de respuesta del sistema (rendimiento)", "PASS",
            f"Respuesta en {duracion:.0f}ms (limite: 3000ms)")
    elif resp.status_code == 200:
        log("TC-AUTO-17", "Tiempo de respuesta del sistema (rendimiento)", "FAIL",
            f"Respuesta lenta: {duracion:.0f}ms (limite: 3000ms)")
    else:
        log("TC-AUTO-17", "Tiempo de respuesta del sistema (rendimiento)", "FAIL",
            f"HTTP {resp.status_code}")

# ── TC-AUTO-18: Eliminacion de libro de prueba (TC-018) ──────────────────────
def tc_auto_18(token):
    if not libro_prueba_id:
        log("TC-AUTO-18", "Eliminacion de libro de prueba del catalogo", "FAIL",
            "No hay libro de prueba para eliminar")
        return
    resp = requests.delete(f"{BASE_URL}/Computer/{libro_prueba_id}", headers=h(token))
    if resp.status_code in [200, 204]:
        log("TC-AUTO-18", "Eliminacion de libro de prueba del catalogo", "PASS",
            f"Libro ID {libro_prueba_id} eliminado correctamente del catalogo")
    else:
        log("TC-AUTO-18", "Eliminacion de libro de prueba del catalogo", "FAIL",
            f"HTTP {resp.status_code}")

# ── Reporte final ─────────────────────────────────────────────────────────────
def generar_reporte():
    total = len(resultados)
    aprobados = sum(1 for r in resultados if r["estado"] == "PASS")
    fallidos = total - aprobados
    porcentaje = (aprobados / total * 100) if total > 0 else 0

    reporte = {
        "fecha_ejecucion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "equipo": "Perez Huarachi Daniel | Palomino Sandoval Anderson | Sarmiento Castro Luis",
        "curso": "Pruebas de Software - UTP",
        "sistema": "GLPI Biblioteca - http://localhost:8080",
        "resumen": {
            "total": total,
            "aprobados": aprobados,
            "fallidos": fallidos,
            "porcentaje_exito": f"{porcentaje:.1f}%"
        },
        "casos": resultados
    }

    with open("reporte_automatizado.json", "w", encoding="utf-8") as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)

    print("\n" + "="*60)
    print("  REPORTE DE PRUEBAS AUTOMATIZADAS")
    print("="*60)
    print(f"  Sistema  : GLPI Biblioteca")
    print(f"  Fecha    : {reporte['fecha_ejecucion']}")
    print(f"  Total    : {total} casos")
    print(f"  PASS     : {aprobados}")
    print(f"  FAIL     : {fallidos}")
    print(f"  Resultado: {porcentaje:.1f}% de exito")
    print("="*60)
    print("  Reporte guardado en: reporte_automatizado.json")

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("="*60)
    print("  PRUEBAS AUTOMATIZADAS - SISTEMA BIBLIOTECARIO GLPI")
    print("  Curso: Pruebas de Software - UTP")
    print("  18 Casos de Prueba via API REST")
    print("="*60 + "\n")

    token = None
    try:
        print("[ Ejecutando 18 casos de prueba... ]\n")
        tc_auto_10()
        tc_auto_11()
        token = iniciar_sesion()
        if token:
            tc_auto_01(token)
            tc_auto_02(token)
            tc_auto_03(token)
            tc_auto_04(token)
            tc_auto_05(token)
            tc_auto_06(token)
            tc_auto_07(token)
            tc_auto_08(token)
            tc_auto_09(token)
            tc_auto_12(token)
            tc_auto_13(token)
            tc_auto_14(token)
            tc_auto_15(token)
            tc_auto_16(token)
            tc_auto_17(token)
            tc_auto_18(token)
        else:
            print("  [ERROR] No se pudo iniciar sesion en GLPI")
    finally:
        if token:
            cerrar_sesion(token)
        generar_reporte()
