# controlador/dashboard_controlador.py
from Modelo.dashboard_modelo import (
    obtener_ingresos_dia,
    obtener_estado_inventario
)
# Junta todos los datos necesarios de ingresos de hoy y ayer, estado de inventario y lo coloca en obtener_datos_dashboard
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
