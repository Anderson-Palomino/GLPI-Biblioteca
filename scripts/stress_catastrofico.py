"""
PRUEBA DE ESTRES CATASTROFICA - GLPI Biblioteca
Equipo: Perez Huarachi Daniel | Palomino Sandoval Anderson | Sarmiento Castro Luis
Curso: Pruebas de Software - UTP

Monitorea durante el ataque:
- CPU del contenedor GLPI y MySQL
- Memoria RAM consumida
- Trafico de red entrante y saliente
- Conexiones TCP en estado TIME_WAIT/CLOSE_WAIT
- Errores de conectividad (timeouts, rechazos, 5xx)
- Punto exacto de saturacion del hardware
"""

import requests
import time
import statistics
import json
import subprocess
import threading
import concurrent.futures
from datetime import datetime
from collections import Counter

BASE_URL = "http://localhost:8080/apirest.php"
APP_TOKEN = "QeoDpRHCafYbpLJQb15IjZIyUQyNyccuxR97X3r1"
USER = "glpi"
PASSWORD = "glpi"

monitoring_active = False
hardware_samples = []

def iniciar_sesion():
    resp = requests.get(
        f"{BASE_URL}/initSession",
        headers={"App-Token": APP_TOKEN},
        auth=(USER, PASSWORD),
        timeout=10
    )
    return resp.json()["session_token"] if resp.status_code == 200 else None

def cerrar_sesion(token):
    try:
        requests.get(f"{BASE_URL}/killSession",
                     headers={"App-Token": APP_TOKEN, "Session-Token": token},
                     timeout=10)
    except:
        pass

def capturar_hardware():
    try:
        result = subprocess.run(
            ["docker", "stats", "--no-stream", "--format",
             "{{.Name}}|{{.CPUPerc}}|{{.MemUsage}}|{{.MemPerc}}|{{.NetIO}}|{{.BlockIO}}"],
            capture_output=True, text=True, timeout=5
        )
        stats = {}
        for line in result.stdout.strip().split("\n"):
            parts = line.split("|")
            if len(parts) >= 6:
                name = parts[0]
                stats[name] = {
                    "cpu": parts[1],
                    "mem_uso": parts[2],
                    "mem_pct": parts[3],
                    "net_io": parts[4],
                    "block_io": parts[5]
                }
        return stats
    except Exception as e:
        return {"error": str(e)[:50]}

def monitor_hardware():
    while monitoring_active:
        sample = capturar_hardware()
        sample["timestamp"] = datetime.now().strftime("%H:%M:%S")
        hardware_samples.append(sample)
        time.sleep(1)

def peticion_con_diagnostico(token):
    inicio = time.time()
    try:
        resp = requests.get(
            f"{BASE_URL}/Computer",
            headers={"App-Token": APP_TOKEN, "Session-Token": token},
            params={"range": "0-10"},
            timeout=15
        )
        duracion_ms = (time.time() - inicio) * 1000
        return {
            "duracion_ms": duracion_ms,
            "status": resp.status_code,
            "exito": resp.status_code in [200, 206],
            "tipo_error": None
        }
    except requests.exceptions.Timeout:
        return {"duracion_ms": (time.time() - inicio) * 1000, "exito": False, "tipo_error": "TIMEOUT"}
    except requests.exceptions.ConnectionError as e:
        if "RemoteDisconnected" in str(e):
            tipo = "CONEXION_CERRADA_POR_SERVIDOR"
        elif "Connection refused" in str(e):
            tipo = "CONEXION_RECHAZADA"
        elif "Read timed out" in str(e):
            tipo = "READ_TIMEOUT"
        else:
            tipo = "ERROR_CONEXION"
        return {"duracion_ms": (time.time() - inicio) * 1000, "exito": False, "tipo_error": tipo}
    except Exception as e:
        return {"duracion_ms": (time.time() - inicio) * 1000, "exito": False, "tipo_error": str(type(e).__name__)}

def ejecutar_ataque(token, num_peticiones, num_concurrentes, nombre_fase):
    print(f"\n[ ATAQUE: {nombre_fase} ]")
    print(f"  Lanzando {num_peticiones} peticiones con {num_concurrentes} usuarios concurrentes...")

    hw_inicio = capturar_hardware()
    inicio_total = time.time()
    resultados = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrentes) as executor:
        futures = [executor.submit(peticion_con_diagnostico, token) for _ in range(num_peticiones)]
        for future in concurrent.futures.as_completed(futures):
            resultados.append(future.result())

    duracion_total = time.time() - inicio_total
    hw_fin = capturar_hardware()
    duraciones = [r["duracion_ms"] for r in resultados]
    exitos = [r for r in resultados if r["exito"]]
    fallos = [r for r in resultados if not r["exito"]]
    tipos_error = Counter(r["tipo_error"] for r in fallos if r["tipo_error"])

    metricas = {
        "fase": nombre_fase,
        "peticiones": num_peticiones,
        "concurrentes": num_concurrentes,
        "duracion_total_seg": round(duracion_total, 2),
        "throughput_req_seg": round(num_peticiones / duracion_total, 2),
        "tiempo_promedio_ms": round(statistics.mean(duraciones), 2),
        "tiempo_max_ms": round(max(duraciones), 2),
        "p95_ms": round(sorted(duraciones)[int(len(duraciones) * 0.95) - 1], 2),
        "p99_ms": round(sorted(duraciones)[int(len(duraciones) * 0.99) - 1], 2),
        "exitos": len(exitos),
        "fallos": len(fallos),
        "tasa_exito": f"{(len(exitos)/len(resultados)*100):.1f}%",
        "tipos_de_error": dict(tipos_error),
        "hardware_inicio": hw_inicio,
        "hardware_fin": hw_fin
    }

    # Output catastrofico
    print(f"  >> Throughput        : {metricas['throughput_req_seg']} req/s")
    print(f"  >> Tiempo promedio   : {metricas['tiempo_promedio_ms']} ms")
    print(f"  >> Tiempo MAXIMO     : {metricas['tiempo_max_ms']} ms {'!!!! CRITICO' if metricas['tiempo_max_ms'] > 5000 else ''}")
    print(f"  >> Latencia p99      : {metricas['p99_ms']} ms")
    print(f"  >> Tasa de exito     : {metricas['tasa_exito']}")

    if fallos:
        print(f"  >> PETICIONES FALLIDAS: {len(fallos)}/{num_peticiones}")
        for tipo, cantidad in tipos_error.most_common(5):
            print(f"     - {tipo}: {cantidad}")

    if hw_fin and "glpi" in hw_fin:
        print(f"  >> GLPI         : CPU {hw_fin['glpi']['cpu']}, RAM {hw_fin['glpi']['mem_uso']}")
    if hw_fin and "glpi-mysql" in hw_fin:
        print(f"  >> MySQL        : CPU {hw_fin['glpi-mysql']['cpu']}, RAM {hw_fin['glpi-mysql']['mem_uso']}")

    return metricas

def main():
    global monitoring_active

    print("="*70)
    print("  PRUEBA DE ESTRES CATASTROFICA - GLPI BIBLIOTECA")
    print("  Curso: Pruebas de Software - UTP")
    print("  Objetivo: Encontrar el LIMITE FISICO del servidor")
    print("="*70)

    print("\n[ ESTADO INICIAL DEL HARDWARE ]")
    hw_inicial = capturar_hardware()
    if "glpi" in hw_inicial:
        print(f"  GLPI    : CPU {hw_inicial['glpi']['cpu']:>8}, RAM {hw_inicial['glpi']['mem_uso']:>20}")
    if "glpi-mysql" in hw_inicial:
        print(f"  MySQL   : CPU {hw_inicial['glpi-mysql']['cpu']:>8}, RAM {hw_inicial['glpi-mysql']['mem_uso']:>20}")

    token = iniciar_sesion()
    if not token:
        print("\n[ERROR FATAL] GLPI no responde - posiblemente caido")
        return

    monitoring_active = True
    monitor_thread = threading.Thread(target=monitor_hardware, daemon=True)
    monitor_thread.start()

    fases = []
    fases.append(ejecutar_ataque(token, 100, 50, "Carga Normal (50 conc.)"))
    fases.append(ejecutar_ataque(token, 500, 250, "Hora Pico (250 conc.)"))
    fases.append(ejecutar_ataque(token, 2000, 1000, "Hora Pico Universidad (1000 conc.)"))
    fases.append(ejecutar_ataque(token, 5000, 2500, "Black Friday (2500 conc.)"))
    fases.append(ejecutar_ataque(token, 10000, 5000, "Ataque DDoS Simulado (5000 conc.)"))
    fases.append(ejecutar_ataque(token, 20000, 10000, "APOCALIPSIS (10000 conc.)"))

    monitoring_active = False
    monitor_thread.join(timeout=2)

    # Analisis catastrofico
    print("\n" + "="*70)
    print("  ANALISIS CATASTROFICO - QUE SE ROMPIO EN GLPI")
    print("="*70)

    cpu_pico = 0
    mem_pico_glpi = "0"
    for sample in hardware_samples:
        if "glpi" in sample:
            try:
                cpu = float(sample["glpi"]["cpu"].replace("%", ""))
                if cpu > cpu_pico:
                    cpu_pico = cpu
                    mem_pico_glpi = sample["glpi"]["mem_uso"]
            except:
                pass

    print(f"\n  PICO DE CPU GLPI         : {cpu_pico:.1f}%")
    print(f"  RAM EN PICO              : {mem_pico_glpi}")
    print(f"  MUESTRAS RECOLECTADAS    : {len(hardware_samples)}")

    print(f"\n  TABLA DE DEGRADACION:")
    print(f"  {'Fase':<40} {'Avg':<8} {'Max':<8} {'Exito':<8} {'Errores'}")
    print(f"  {'-'*40} {'-'*7} {'-'*7} {'-'*7} {'-'*30}")
    for f in fases:
        errores_resumen = ", ".join(f"{k}:{v}" for k, v in list(f["tipos_de_error"].items())[:2])
        print(f"  {f['fase']:<40} {f['tiempo_promedio_ms']:<8.0f} {f['tiempo_max_ms']:<8.0f} {f['tasa_exito']:<8} {errores_resumen[:30]}")

    # Conclusion catastrofica
    print(f"\n  CONCLUSION:")
    fase_quiebre = None
    for f in fases:
        if float(f["tasa_exito"].replace("%", "")) < 50:
            fase_quiebre = f
            break

    if fase_quiebre:
        print(f"  >> El sistema COLAPSO en la fase: {fase_quiebre['fase']}")
        print(f"  >> {fase_quiebre['fallos']} de {fase_quiebre['peticiones']} peticiones fallaron")
        print(f"  >> Tipos de error detectados: {fase_quiebre['tipos_de_error']}")
        print(f"  >> En produccion esto significaria: usuarios viendo errores 503/504,")
        print(f"     sesiones perdidas, transacciones incompletas, datos inconsistentes")
    else:
        print(f"  >> El sistema resistio todas las fases (CPU pico: {cpu_pico:.1f}%)")

    reporte = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "equipo": "Perez Huarachi Daniel | Palomino Sandoval Anderson | Sarmiento Castro Luis",
        "tipo_prueba": "Estres Catastrofico con monitoreo de hardware",
        "cpu_pico_porcentaje": cpu_pico,
        "memoria_pico": mem_pico_glpi,
        "fases": fases,
        "muestras_hardware": hardware_samples
    }

    with open("reporte_catastrofico.json", "w", encoding="utf-8") as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2, default=str)

    print(f"\n  Reporte completo: reporte_catastrofico.json")
    print("="*70)

    cerrar_sesion(token)

if __name__ == "__main__":
    main()
