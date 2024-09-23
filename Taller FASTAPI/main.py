from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from asyncpg.exceptions import DataError, UniqueViolationError
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

class FullDataset(BaseModel):
    url: str
    source: str
    label: str
    url_length: int
    starts_with_ip: bool
    url_entropy: float
    has_punycode: bool
    digit_letter_ratio: float
    dot_count: int
    at_count: int
    dash_count: int
    tld_count: int
    domain_has_digits: bool
    subdomain_count: int
    nan_char_entropy: float
    has_internal_links: bool
    whois_data: str
    domain_age_days: float

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
    try:
        offset = (page - 1) * limit
        rows = await app.state.db.fetch(f"""
            SELECT url, label, url_length, domain_has_digits, domain_age_days 
            FROM dataset_phishing 
            LIMIT $1 OFFSET $2;
        """, limit, offset)

        # Se lanza cuando no se encuentran registros
        if not rows:
                raise HTTPException(status_code=404, detail="No records found")

        return ResponseModel(
            data=[Dataset(**row) for row in rows],
            page=page,
            limit=limit
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        # General error
        raise HTTPException(status_code=500, detail="Internal server error")



# Punto 5
@app.post("/dataset")
async def insert_dataset(datasets: List[FullDataset]):
    insert_query = """
            INSERT INTO dataset_phishing (
                url, source, label, url_length, starts_with_ip, url_entropy, has_punycode, 
                digit_letter_ratio, dot_count, at_count, dash_count, tld_count, domain_has_digits, 
                subdomain_count, nan_char_entropy, has_internal_links, whois_data, domain_age_days
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18
            );
        """
    try:
        if not datasets:
            raise HTTPException(status_code=400, detail="No dataset provided")

        for dataset in datasets:
            await app.state.db.execute(insert_query, 
                dataset.url, dataset.source, dataset.label, dataset.url_length, 
                dataset.starts_with_ip, dataset.url_entropy, dataset.has_punycode, 
                dataset.digit_letter_ratio, dataset.dot_count, dataset.at_count, 
                dataset.dash_count, dataset.tld_count, dataset.domain_has_digits, 
                dataset.subdomain_count, dataset.nan_char_entropy, dataset.has_internal_links, 
                dataset.whois_data, dataset.domain_age_days
            )

        total_records = await app.state.db.fetchval("SELECT COUNT(*) FROM dataset_phishing")

        return {
            "message": f"{len(datasets)} records inserted successfully",
            "inserted_records": len(datasets),
            "total_records": total_records
        }
    except DataError as e:
        raise HTTPException(status_code=400, detail="Data error: invalid data format")
    except UniqueViolationError as e:
        raise HTTPException(status_code=400, detail="Unique constraint violation: duplicated data")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Puedes modificar el contenido del mensaje como prefieras
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Faltan campos en el request body",
        },
    )