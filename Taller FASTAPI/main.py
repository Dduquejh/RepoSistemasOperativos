from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import asyncpg
import os
from dotenv import load_dotenv
from typing import List

class Dataset(BaseModel):
    url: str
    label: str
    url_length: int
    domain_has_digits: bool
    domain_age_days: float

class ResponseModel(BaseModel):
    data: List[Dataset]
    page: int
    limit: int

load_dotenv()

# Obtener la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear la aplicación FastAPI
app = FastAPI()

# Función para obtener una conexión a la base de datos
async def get_connection():
    return await asyncpg.connect(DATABASE_URL)

# Eventos de inicio y cierre de la aplicación
@app.on_event("startup")
async def startup_event():
    app.state.db = await get_connection()

@app.on_event("shutdown")
async def shutdown_event():
    await app.state.db.close()

# Ruta para obtener los datos del dataset
@app.get("/dataset", response_model=ResponseModel)
async def read_dataset(page: int = Query(1, ge=1), limit: int = Query(1, le=100)):
    offset = (page - 1) * limit
    rows = await app.state.db.fetch(f"""
        SELECT url, label, url_length, domain_has_digits, domain_age_days 
        FROM dataset_phishing 
        LIMIT $1 OFFSET $2;
    """, limit, offset)

    return ResponseModel(
        data=[Dataset(**row) for row in rows],
        page=page,
        limit=limit
    )
