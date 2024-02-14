import logging
import requests
import json

from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import datetime
from app.models.model import AppointmentModel
from app.config import settings

router = APIRouter(
    tags=["dentalink"],
    responses={404: {"description": "Not found"}},
)

@router.get("/citas")
async def citas(Data: AppointmentModel = None) -> JSONResponse:
    Appointments = []
    logging.info("Requesting citas")
    logging.info(Data)
    headers = {
        'Authorization': 'Token ' + settings.app_token
    }
    if not Data:
        logging.info("No query")
        url = settings.url_citas
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            logging.error(response.text)
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Error al obtener citas"})
        response = json.loads(response.text)
        Appointments = Appointments + response["data"]
    else:
        query = {}

        logging.info(Data)
        if Data.fecha_inicio:
            if Data.fecha_fin:
                query["fecha"] = [{"gte": Data.fecha_inicio.strftime("%Y-%m-%d")}, {"lte": Data.fecha_fin.strftime("%Y-%m-%d")}]
            else:
                query["fecha"] = {"eq": Data.fecha_inicio.strftime("%Y-%m-%d")}
        if Data.id_estado_cita:
            for ide in Data.id_estado_cita:
                query["id_estado"] = {"eq": ide}
                url = settings.url_citas+'?q='+json.dumps(query)
                logging.info(url)
                response = requests.get(url, headers=headers)
                if response.status_code != 200:
                    logging.error(response.text)
                    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Error al obtener citas"})
                response = json.loads(response.text)
                Appointments = Appointments + response["data"]
            if Data.id_sucursales:
                Appointments = [cita for cita in Appointments if cita["id_sucursal"] in Data.id_sucursales]
        else:
            url = settings.url_citas+'?q='+json.dumps(query)
            logging.info(url)
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                logging.error(response.text)
                return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Error al obtener citas"})
            response = json.loads(response.text)
            Appointments = Appointments + response["data"]
        if not Data.fecha_inicio and not Data.id_estado_cita and Data.id_sucursales:
            url = settings.url_citas
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                logging.error(response.text)
                return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Error al obtener citas"})
            response = json.loads(response.text)
            Appointments = Appointments + response["data"]
            Appointments = [cita for cita in Appointments if cita["id_sucursal"] in Data.id_sucursales]

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(Appointments))