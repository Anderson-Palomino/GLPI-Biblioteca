"""
Pruebas Automatizadas - Sistema Bibliotecario GLPI
Equipo: Perez Huarachi Daniel | Palomino Sandoval Anderson | Sarmiento Castro Luis
Curso: Pruebas de Software - UTP
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8080/apirest.php"
APP_TOKEN = "QeoDpRHCafYbpLJQb15IjZIyUQyNyccuxR97X3r1"
USER = "glpi"
PASSWORD = "glpi"

resultados = []

def log(tc_id, nombre, estado, detalle=""):
    icon = "[PASS]" if estado == "PASS" else "[FAIL]"
    print(f"  {icon} | {tc_id} - {nombre}")
    if detalle:
        print(f"         {detalle}")
    resultados.append({"id": tc_id, "nombre": nombre, "estado": estado, "detalle": detalle})

def iniciar_sesion():
    resp = requests.get(
        f"{BASE_URL}/initSession",
        headers={"App-Token": APP_TOKEN},
        auth=(USER, PASSWORD)
    )
    if resp.status_code == 200:
        return resp.json()["session_token"]
    raise Exception(f"Login fallido: {resp.text}")

def cerrar_sesion(token):
    requests.get(
        f"{BASE_URL}/killSession",
        headers={"App-Token": APP_TOKEN, "Session-Token": token}
    )

def headers(token):
    return {"App-Token": APP_TOKEN, "Session-Token": token, "Content-Type": "application/json"}

# ── TC-AUTO-01: Autenticación válida ──────────────────────────────────────────
def tc_auto_01():
    try:
        token = iniciar_sesion()
        if token and len(token) > 10:
            log("TC-AUTO-01", "Autenticación con credenciales válidas", "PASS", f"Session token obtenido: {token[:20]}...")
        else:
            log("TC-AUTO-01", "Autenticación con credenciales válidas", "FAIL", "Token inválido")
        return token
    except Exception as e:
        log("TC-AUTO-01", "Autenticación con credenciales válidas", "FAIL", str(e))
        return None

# ── TC-AUTO-02: Autenticación inválida ───────────────────────────────────────
def tc_auto_02():
    resp = requests.get(
        f"{BASE_URL}/initSession",
        headers={"App-Token": APP_TOKEN},
        auth=("glpi", "password_incorrecta")
    )
    if resp.status_code in [400, 401]:
        log("TC-AUTO-02", "Autenticación con credenciales inválidas", "PASS", f"Sistema rechazó correctamente (HTTP {resp.status_code})")
    else:
        log("TC-AUTO-02", "Autenticación con credenciales inválidas", "FAIL", f"Sistema aceptó credenciales inválidas (HTTP {resp.status_code})")

# ── TC-AUTO-03: Listar libros del catálogo ───────────────────────────────────
def tc_auto_03(token):
    resp = requests.get(
        f"{BASE_URL}/Computer",
        headers=headers(token),
        params={"range": "0-50"}
    )
    if resp.status_code == 200:
        libros = resp.json()
        count = len(libros)
        if count >= 12:
            log("TC-AUTO-03", "Catálogo de libros accesible via API", "PASS", f"{count} activos encontrados en el catálogo")
        else:
            log("TC-AUTO-03", "Catálogo de libros accesible via API", "FAIL", f"Solo {count} activos (esperado >= 12)")
    else:
        log("TC-AUTO-03", "Catálogo de libros accesible via API", "FAIL", f"HTTP {resp.status_code}")
    return resp.json() if resp.status_code == 200 else []

# ── TC-AUTO-04: Registro de nuevo libro ──────────────────────────────────────
def tc_auto_04(token):
    payload = {
        "input": {
            "name": "Libro Automatizado - Test",
            "serial": "ISBN-TEST-AUTO-001",
            "comment": "Creado por script de pruebas automatizadas"
        }
    }
    resp = requests.post(f"{BASE_URL}/Computer", headers=headers(token), json=payload)
    if resp.status_code == 201:
        libro_id = resp.json()["id"]
        log("TC-AUTO-04", "Registro de libro via API", "PASS", f"Libro creado con ID: {libro_id}")
        return libro_id
    else:
        log("TC-AUTO-04", "Registro de libro via API", "FAIL", f"HTTP {resp.status_code}: {resp.text[:100]}")
        return None

# ── TC-AUTO-05: Eliminar libro de prueba ─────────────────────────────────────
def tc_auto_05(token, libro_id):
    if not libro_id:
        log("TC-AUTO-05", "Eliminación de libro de prueba", "FAIL", "No hay ID de libro para eliminar")
        return
    resp = requests.delete(f"{BASE_URL}/Computer/{libro_id}", headers=headers(token))
    if resp.status_code in [200, 204]:
        log("TC-AUTO-05", "Eliminación de libro de prueba", "PASS", f"Libro ID {libro_id} eliminado correctamente")
    else:
        log("TC-AUTO-05", "Eliminación de libro de prueba", "FAIL", f"HTTP {resp.status_code}")

# ── TC-AUTO-06: Listar tickets de préstamo ───────────────────────────────────
def tc_auto_06(token):
    resp = requests.get(f"{BASE_URL}/Ticket", headers=headers(token), params={"range": "0-50"})
    if resp.status_code == 200:
        tickets = resp.json()
        count = len(tickets)
        if count >= 4:
            log("TC-AUTO-06", "Tickets de préstamo accesibles via API", "PASS", f"{count} tickets encontrados")
        else:
            log("TC-AUTO-06", "Tickets de préstamo accesibles via API", "FAIL", f"Solo {count} tickets (esperado >= 4)")
    else:
        log("TC-AUTO-06", "Tickets de préstamo accesibles via API", "FAIL", f"HTTP {resp.status_code}")

# ── TC-AUTO-07: Préstamo duplicado (BUG-002) ─────────────────────────────────
def tc_auto_07(token):
    payload = {
        "input": {
            "name": "Prestamo Duplicado - Test Automatizado",
            "content": "Verificacion automatica de BUG-002: prestamo duplicado",
            "status": 1,
            "type": 1
        }
    }
    resp1 = requests.post(f"{BASE_URL}/Ticket", headers=headers(token), json=payload)
    resp2 = requests.post(f"{BASE_URL}/Ticket", headers=headers(token), json=payload)

    if resp1.status_code == 201 and resp2.status_code == 201:
        id1, id2 = resp1.json()["id"], resp2.json()["id"]
        log("TC-AUTO-07", "Validación préstamo duplicado (BUG-002)", "FAIL",
            f"BUG confirmado: sistema creó dos tickets duplicados (ID {id1} y {id2}). GLPI no valida duplicados.")
        # Limpiar tickets de prueba
        requests.delete(f"{BASE_URL}/Ticket/{id1}", headers=headers(token))
        requests.delete(f"{BASE_URL}/Ticket/{id2}", headers=headers(token))
    else:
        log("TC-AUTO-07", "Validación préstamo duplicado (BUG-002)", "PASS", "Sistema rechazó el préstamo duplicado")

# ── Reporte final ─────────────────────────────────────────────────────────────
def generar_reporte():
    total = len(resultados)
    aprobados = sum(1 for r in resultados if r["estado"] == "PASS")
    fallidos = total - aprobados
    porcentaje = (aprobados / total * 100) if total > 0 else 0

    reporte = {
        "fecha_ejecucion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "equipo": "Perez Huarachi Daniel | Palomino Sandoval Anderson | Sarmiento Castro Luis",
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
    print(f"  PASS  : {aprobados}")
    print(f"  FAIL  : {fallidos}")
    print(f"  Resultado: {porcentaje:.1f}% de éxito")
    print("="*60)
    print("  Reporte guardado en: reporte_automatizado.json")

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("="*60)
    print("  PRUEBAS AUTOMATIZADAS - SISTEMA BIBLIOTECARIO GLPI")
    print("  Curso: Pruebas de Software - UTP")
    print("="*60 + "\n")

    token = None
    try:
        print("[ Ejecutando casos de prueba... ]\n")
        tc_auto_02()
        token = tc_auto_01()
        if token:
            tc_auto_03(token)
            libro_id = tc_auto_04(token)
            tc_auto_05(token, libro_id)
            tc_auto_06(token)
            tc_auto_07(token)
    finally:
        if token:
            cerrar_sesion(token)
        generar_reporte()
