import logging
import requests
import json
from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import datetime
from app.models.model import AppointmentModel, StateAppointmentModel
from app.config import settings

router = APIRouter(
    tags=["dentalink"],
    responses={404: {"description": "Not found"}},
)

@router.get("/citas")
async def citas(Data: AppointmentModel = None) -> JSONResponse:
    Appointments = []
    logging.info("Requesting appointments...")
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
        logging.info("Querying appointments...")
        if Data.fecha_inicio:
            logging.info("Has date")
            logging.debug(f'Fecha inicio: {Data.fecha_inicio}')
            if Data.fecha_fin:
                logging.debug(f'Fecha fin: {Data.fecha_fin}')
                query["fecha"] = [{"gte": Data.fecha_inicio.strftime("%Y-%m-%d")}, {"lte": Data.fecha_fin.strftime("%Y-%m-%d")}]
            else:
                query["fecha"] = {"eq": Data.fecha_inicio.strftime("%Y-%m-%d")}
        if Data.id_estado_cita:
            logging.info("Has state(s)")
            logging.debug(f'Estados: {Data.id_estado_cita}')
            for ide in Data.id_estado_cita:
                query["id_estado"] = {"eq": ide}
                url = settings.url_citas+'?q='+json.dumps(query)
                logging.debug(f'URL id estado: {url}')
                response = requests.get(url, headers=headers)
                if response.status_code != 200:
                    logging.error(response.text)
                    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Error al obtener citas"})
                response = json.loads(response.text)
                Appointments = Appointments + response["data"]
            if Data.id_sucursales:
                Appointments = [cita for cita in Appointments if cita["id_sucursal"] in Data.id_sucursales]
        else:
            logging.info("No states")
            url = settings.url_citas+'?q='+json.dumps(query)
            logging.debug(f'URL: {url}')
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                logging.error(response.text)
                return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Error al obtener citas"})
            response = json.loads(response.text)
            Appointments = Appointments + response["data"]
        if Data.id_sucursales:
            Appointments = [cita for cita in Appointments if cita["id_sucursal"] in Data.id_sucursales]

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(Appointments))

@router.put("/estado_citas")
async def change_state_appointments(State:StateAppointmentModel = None) -> JSONResponse:
    
    if not State:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "No se ha enviado el estado de la cita"})
    logging.info("Changing state of appointment...")
    logging.debug(f'ID Cita: {State.id_cita}')
    logging.debug(f'ID Estado: {State.id_estado}')
    logging.debug(f'Comentarios: {State.comentarios}')
    headers = {
        'Authorization': 'Token ' + settings.app_token
    }
    url = settings.url_citas +'/'+ str(State.id_cita)
    logging.debug(f'URL: {url}')
    data = {
        "id_estado": State.id_estado,
        "comentarios": State.comentarios
    }
    logging.debug(f'Data: {data}')
    response = requests.put(url, headers=headers, data=data)
    if response.status_code != 200:
        logging.error(response.text)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Error al cambiar estado de cita"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(response.json()))