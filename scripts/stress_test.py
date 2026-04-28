"""
Prueba de Estres y Rendimiento - GLPI Biblioteca
Equipo: Perez Huarachi Daniel | Palomino Sandoval Anderson | Sarmiento Castro Luis
Curso: Pruebas de Software - UTP

Mide:
- Tiempo de respuesta bajo carga incremental (10, 50, 100, 200 peticiones concurrentes)
- Tasa de exito vs fallos durante el estres
- Tiempo de estabilizacion post-estres
"""

import requests
import time
import statistics
import json
import concurrent.futures
from datetime import datetime

BASE_URL = "http://localhost:8080/apirest.php"
APP_TOKEN = "QeoDpRHCafYbpLJQb15IjZIyUQyNyccuxR97X3r1"
USER = "glpi"
PASSWORD = "glpi"

def iniciar_sesion():
    resp = requests.get(
        f"{BASE_URL}/initSession",
        headers={"App-Token": APP_TOKEN},
        auth=(USER, PASSWORD),
        timeout=10
    )
    return resp.json()["session_token"] if resp.status_code == 200 else None

def cerrar_sesion(token):
    requests.get(f"{BASE_URL}/killSession",
                 headers={"App-Token": APP_TOKEN, "Session-Token": token},
                 timeout=10)

def peticion_unica(token):
    inicio = time.time()
    try:
        resp = requests.get(
            f"{BASE_URL}/Computer",
            headers={"App-Token": APP_TOKEN, "Session-Token": token},
            params={"range": "0-10"},
            timeout=30
        )
        duracion_ms = (time.time() - inicio) * 1000
        exito = resp.status_code in [200, 206]
        return {"duracion_ms": duracion_ms, "exito": exito, "status": resp.status_code}
    except Exception as e:
        duracion_ms = (time.time() - inicio) * 1000
        return {"duracion_ms": duracion_ms, "exito": False, "error": str(e)[:50]}

def ejecutar_carga(token, num_peticiones, num_concurrentes):
    print(f"\n[ Ejecutando {num_peticiones} peticiones con {num_concurrentes} concurrentes ]")
    inicio_total = time.time()
    resultados = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrentes) as executor:
        futures = [executor.submit(peticion_unica, token) for _ in range(num_peticiones)]
        for future in concurrent.futures.as_completed(futures):
            resultados.append(future.result())

    duracion_total = time.time() - inicio_total
    duraciones = [r["duracion_ms"] for r in resultados]
    exitos = sum(1 for r in resultados if r["exito"])
    fallos = len(resultados) - exitos

    metricas = {
        "peticiones": num_peticiones,
        "concurrentes": num_concurrentes,
        "duracion_total_seg": round(duracion_total, 2),
        "throughput_req_seg": round(num_peticiones / duracion_total, 2),
        "tiempo_promedio_ms": round(statistics.mean(duraciones), 2),
        "tiempo_min_ms": round(min(duraciones), 2),
        "tiempo_max_ms": round(max(duraciones), 2),
        "tiempo_mediana_ms": round(statistics.median(duraciones), 2),
        "p95_ms": round(sorted(duraciones)[int(len(duraciones) * 0.95) - 1], 2),
        "p99_ms": round(sorted(duraciones)[int(len(duraciones) * 0.99) - 1], 2),
        "exitos": exitos,
        "fallos": fallos,
        "tasa_exito": f"{(exitos/len(resultados)*100):.1f}%"
    }

    print(f"  Duracion total      : {metricas['duracion_total_seg']}s")
    print(f"  Throughput          : {metricas['throughput_req_seg']} req/s")
    print(f"  Tiempo promedio     : {metricas['tiempo_promedio_ms']} ms")
    print(f"  Tiempo minimo       : {metricas['tiempo_min_ms']} ms")
    print(f"  Tiempo maximo       : {metricas['tiempo_max_ms']} ms")
    print(f"  Mediana (p50)       : {metricas['tiempo_mediana_ms']} ms")
    print(f"  Percentil 95 (p95)  : {metricas['p95_ms']} ms")
    print(f"  Percentil 99 (p99)  : {metricas['p99_ms']} ms")
    print(f"  Tasa de exito       : {metricas['tasa_exito']} ({exitos}/{len(resultados)})")

    return metricas

def medir_estabilizacion(token, baseline_ms, max_intentos=20):
    print(f"\n[ Midiendo tiempo de estabilizacion (baseline: {baseline_ms:.0f}ms) ]")
    print("  Esperando que el sistema vuelva al tiempo base...")

    inicio = time.time()
    intentos = 0
    while intentos < max_intentos:
        time.sleep(0.5)
        muestra = peticion_unica(token)
        intentos += 1
        if muestra["exito"] and muestra["duracion_ms"] <= baseline_ms * 1.5:
            tiempo_estabilizacion = time.time() - inicio
            print(f"  Sistema estabilizado en {tiempo_estabilizacion:.2f}s "
                  f"(intentos: {intentos}, ultima muestra: {muestra['duracion_ms']:.0f}ms)")
            return {
                "tiempo_estabilizacion_seg": round(tiempo_estabilizacion, 2),
                "intentos": intentos,
                "ultima_muestra_ms": round(muestra["duracion_ms"], 2)
            }

    return {
        "tiempo_estabilizacion_seg": time.time() - inicio,
        "intentos": intentos,
        "estabilizado": False
    }

def main():
    print("="*65)
    print("  PRUEBA DE ESTRES Y RENDIMIENTO - GLPI BIBLIOTECA")
    print("  Curso: Pruebas de Software - UTP")
    print("="*65)

    token = iniciar_sesion()
    if not token:
        print("[ERROR] No se pudo iniciar sesion en GLPI")
        return

    fases = []

    # FASE 1: Baseline - 1 peticion para tomar tiempo base
    print("\n[ FASE 1: BASELINE ] Midiendo tiempo de respuesta sin carga")
    baseline = peticion_unica(token)
    print(f"  Tiempo base: {baseline['duracion_ms']:.2f} ms")
    baseline_ms = baseline["duracion_ms"]

    # FASE 2: Carga ligera
    fase2 = ejecutar_carga(token, num_peticiones=20, num_concurrentes=5)
    fase2["fase"] = "Carga Ligera (5 concurrentes)"
    fases.append(fase2)

    # FASE 3: Carga media
    fase3 = ejecutar_carga(token, num_peticiones=50, num_concurrentes=20)
    fase3["fase"] = "Carga Media (20 concurrentes)"
    fases.append(fase3)

    # FASE 4: Carga alta - estres
    fase4 = ejecutar_carga(token, num_peticiones=100, num_concurrentes=50)
    fase4["fase"] = "Estres (50 concurrentes)"
    fases.append(fase4)

    # FASE 5: Carga extrema
    fase5 = ejecutar_carga(token, num_peticiones=200, num_concurrentes=100)
    fase5["fase"] = "Estres Extremo (100 concurrentes)"
    fases.append(fase5)

    # FASE 6: Estres severo - 200 concurrentes
    fase6 = ejecutar_carga(token, num_peticiones=400, num_concurrentes=200)
    fase6["fase"] = "Estres Severo (200 concurrentes)"
    fases.append(fase6)

    # FASE 7: Estres critico - 500 concurrentes
    fase7 = ejecutar_carga(token, num_peticiones=1000, num_concurrentes=500)
    fase7["fase"] = "Estres Critico (500 concurrentes)"
    fases.append(fase7)

    # FASE 8: Punto de quiebre - 1000 concurrentes
    fase8 = ejecutar_carga(token, num_peticiones=2000, num_concurrentes=1000)
    fase8["fase"] = "Punto de Quiebre (1000 concurrentes)"
    fases.append(fase8)

    # FASE 9: Tiempo de estabilizacion
    estabilizacion = medir_estabilizacion(token, baseline_ms, max_intentos=60)

    # Reporte final
    reporte = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "equipo": "Perez Huarachi Daniel | Palomino Sandoval Anderson | Sarmiento Castro Luis",
        "sistema": "GLPI Biblioteca - http://localhost:8080",
        "baseline_ms": round(baseline_ms, 2),
        "fases": fases,
        "estabilizacion_post_estres": estabilizacion
    }

    with open("reporte_stress.json", "w", encoding="utf-8") as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)

    print("\n" + "="*65)
    print("  RESUMEN COMPARATIVO")
    print("="*65)
    print(f"  {'Fase':<35} {'Avg (ms)':<10} {'p95 (ms)':<10} {'Exito'}")
    print(f"  {'-'*35} {'-'*10} {'-'*10} {'-'*10}")
    print(f"  {'Baseline (1 peticion)':<35} {baseline_ms:<10.0f} {'-':<10} {'100%' if baseline['exito'] else '0%'}")
    for f in fases:
        print(f"  {f['fase']:<35} {f['tiempo_promedio_ms']:<10.0f} {f['p95_ms']:<10.0f} {f['tasa_exito']}")
    print("="*65)
    print(f"  Tiempo de estabilizacion post-estres: {estabilizacion['tiempo_estabilizacion_seg']}s")
    print("="*65)
    print("  Reporte completo guardado en: reporte_stress.json")

    cerrar_sesion(token)

if __name__ == "__main__":
    main()
