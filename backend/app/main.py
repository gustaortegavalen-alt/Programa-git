# =============================================================================
# SMARTBUILD - BACKEND API (FASTAPI)
# Motor de Cotización y Compatibilidad de PC
# Aprendiz: Gustavo Andrés Ortega Valencia - ADSO Ficha 3336152
# =============================================================================

from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import os

app = FastAPI(
    title="SmartBuild API",
    description="API REST para cotización y validación de compatibilidad de componentes de PC",
    version="1.0.0"
)

# -----------------------------------------------------------------------------
# Configuración de Base de Datos y Plantillas
# -----------------------------------------------------------------------------
DB_NAME = "database/smartbuild.db"

templates = Jinja2Templates(directory="templates")

def obtener_conexion_db():
    # Asegurar que la carpeta 'database' exista de forma segura
    os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)
    conexion = sqlite3.connect(DB_NAME)
    conexion.row_factory = sqlite3.Row
    try:
        yield conexion
    finally:
        conexion.close()

def inicializar_bd():
    os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS componentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            ram_gb INTEGER
        )
    """)
    conexion.commit()
    conexion.close()

@app.on_event("startup")
def evento_inicio():
    inicializar_bd()

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

class ComponenteEsquema(BaseModel):
    nombre: str
    categoria: str
    precio: float
    ram_gb: Optional[int] = None

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

# Métodos para plantillas HTML
@app.get("/formulario", response_class=HTMLResponse)
async def mostrar_formulario(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "resultado": None})

@app.post("/formulario", response_class=HTMLResponse)
async def procesar_formulario(request: Request, cpu_modelo: str = Form(...), ram_gb: int = Form(...)):
    mensaje = f"Datos procesados con éxito para la CPU: {cpu_modelo} con {ram_gb}GB de RAM."
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "resultado": mensaje
    })

# ==========================================
# OPERACIONES CRUD CON SQLite
# ==========================================

@app.post("/api/componentes")
def crear_componente_api(datos: ComponenteEsquema, db: sqlite3.Connection = Depends(obtener_conexion_db)):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO componentes (nombre, categoria, precio, ram_gb) VALUES (?, ?, ?, ?)",
        (datos.nombre, datos.categoria, datos.precio, datos.ram_gb)
    )
    db.commit()
    return {"mensaje": "Componente registrado correctamente en la base de datos"}

@app.get("/api/componentes", response_model=List[dict])
def consultar_componentes(db: sqlite3.Connection = Depends(obtener_conexion_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM componentes")
    filas = cursor.fetchall()
    return [dict(fila) for fila in filas]

@app.put("/api/componentes/{componente_id}")
def actualizar_componente(componente_id: int, datos: ComponenteEsquema, db: sqlite3.Connection = Depends(obtener_conexion_db)):
    cursor = db.cursor()
    cursor.execute(
        "UPDATE componentes SET nombre = ?, categoria = ?, precio = ?, ram_gb = ? WHERE id = ?",
        (datos.nombre, datos.categoria, datos.precio, datos.ram_gb, componente_id)
    )
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Componente no encontrado")
    return {"mensaje": f"Componente ID {componente_id} actualizado con éxito"}

@app.delete("/api/componentes/{componente_id}")
def eliminar_componente(componente_id: int, db: sqlite3.Connection = Depends(obtener_conexion_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM componentes WHERE id = ?", (componente_id,))
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Componente no encontrado")
    return {"mensaje": f"Componente ID {componente_id} eliminado correctamente"}
