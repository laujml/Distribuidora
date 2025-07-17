# controlador/dashboard_controlador.py
from modelo.dashboard_modelo import (
    obtener_ingresos_dia,
    obtener_estado_inventario
)

def obtener_datos_dashboard():
    from datetime import date, timedelta

    hoy = date.today()
    ayer = hoy - timedelta(days=1)

    ingresos_ayer = obtener_ingresos_dia(ayer)
    ingresos_hoy = obtener_ingresos_dia(hoy)
    inventario = obtener_estado_inventario()

    return {
        "ingresos_ayer": ingresos_ayer,
        "ingresos_hoy": ingresos_hoy,
        "inventario": inventario
    }
