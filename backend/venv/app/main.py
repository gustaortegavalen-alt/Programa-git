# =============================================================================
# SMARTBUILD - BACKEND API (FASTAPI)
# Motor de Cotización y Compatibilidad de PC
# Aprendiz: Gustavo Andrés Ortega Valencia - ADSO Ficha 3336152
# =============================================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="SmartBuild API",
    description="API REST para cotización y validación de compatibilidad de componentes de PC",
    version="1.0.0"
)

# -----------------------------------------------------------------------------
# Modelos de Datos (Schemas con Pydantic)
# -----------------------------------------------------------------------------
class Componente(BaseModel):
    id_componente: int
    categoria: str
    nombre: str
    marca: str
    precio: float
    consumo_tdp_watts: int
    socket: Optional[str] = None
    tipo_ram: Optional[str] = None
    factor_forma: Optional[str] = None
    potencia_watts: Optional[int] = None
    largo_mm: Optional[int] = None

class ResultadoCompatibilidad(BaseModel):
    es_compatible: bool
    consumo_total_watts: int
    potencia_fuente_watts: int
    alertas: List[str]
    mensajes_exito: List[str]

# -----------------------------------------------------------------------------
# Endpoints de la API
# -----------------------------------------------------------------------------

@app.get("/", tags=["General"])
def read_root():
    return {
        "sistema": "SmartBuild API",
        "estado": "Operativo",
        "version": "1.0.0",
        "autor": "Gustavo Andrés Ortega Valencia"
    }

# Endpoint para evaluar compatibilidad técnica entre piezas seleccionadas
@app.post("/api/validar-compatibilidad", response_model=ResultadoCompatibilidad, tags=["Motor de Compatibilidad"])
def validar_compatibilidad(cpu: Componente, motherboard: Componente, ram: Componente, psu: Componente, gpu: Optional[Componente] = None):
    alertas = []
    mensajes_exito = []
    es_compatible = True

    # 1. Regla: Socket CPU == Socket Motherboard
    if cpu.socket and motherboard.socket:
        if cpu.socket.upper() != motherboard.socket.upper():
            es_compatible = False
            alertas.append(f"Incompatibilidad de Socket: La CPU ({cpu.socket}) no encaja en la tarjeta madre ({motherboard.socket}).")
        else:
            mensajes_exito.append(f"Socket compatible: {cpu.socket}.")

    # 2. Regla: Tipo de RAM (DDR4 / DDR5) == Tipo de RAM soportado por Motherboard
    if ram.tipo_ram and motherboard.tipo_ram:
        if ram.tipo_ram.upper() != motherboard.tipo_ram.upper():
            es_compatible = False
            alertas.append(f"Incompatibilidad de RAM: La memoria {ram.tipo_ram} no es compatible con la placa madre ({motherboard.tipo_ram}).")
        else:
            mensajes_exito.append(f"Tipo de memoria RAM compatible: {ram.tipo_ram}.")

    # 3. Regla: Consumo TDP Total <= Vataje de la Fuente de Poder
    consumo_total = cpu.consumo_tdp_watts + ram.consumo_tdp_watts + motherboard.consumo_tdp_watts
    if gpu:
        consumo_total += gpu.consumo_tdp_watts

    # Agregar margen de seguridad recomendado (100W extra)
    consumo_con_margen = consumo_total + 100
    potencia_fuente = psu.potencia_watts or 0

    if potencia_fuente < consumo_con_margen:
        es_compatible = False
        alertas.append(f"Fuente Insuficiente: El sistema consume ~{consumo_total}W (se recomiendan {consumo_con_margen}W con margen) y la fuente seleccionada es de {potencia_fuente}W.")
    else:
        mensajes_exito.append(f"Suministro eléctrico adecuado: Consumo de {consumo_total}W con fuente de {potencia_fuente}W.")

    return ResultadoCompatibilidad(
        es_compatible=es_compatible,
        consumo_total_watts=consumo_total,
        potencia_fuente_watts=potencia_fuente,
        alertas=alertas,
        mensajes_exito=mensajes_exito
    )
from fastapi import Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Configurar la carpeta de plantillas (asegúrate de apuntar a tu carpeta templates)
templates = Jinja2Templates(directory="templates")

# 1. Método GET: Muestra el formulario HTML en el navegador
@app.get("/formulario", response_class=HTMLResponse)
async def mostrar_formulario(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "resultado": None})

# 2. Método POST: Recibe los datos enviados desde el formulario HTML
@app.post("/formulario", response_class=HTMLResponse)
async def procesar_formulario(request: Request, cpu_modelo: str = Form(...), ram_gb: int = Form(...)):
    # Aquí puedes procesar los datos o llamar a tu lógica de validación
    mensaje = f"Datos procesados con éxito para la CPU: {cpu_modelo} con {ram_gb}GB de RAM."
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "resultado": mensaje
    })
