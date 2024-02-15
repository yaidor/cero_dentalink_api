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

@router.get("/get_appointments")
async def appointments(Data: AppointmentModel = None) -> JSONResponse:
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
        if Data.ini_date:
            logging.info("Has date")
            logging.debug(f'Initial date: {Data.ini_date}')
            if Data.end_date:
                logging.debug(f'End date: {Data.end_date}')
                query["fecha"] = [{"gte": Data.ini_date.strftime("%Y-%m-%d")}, {"lte": Data.end_date.strftime("%Y-%m-%d")}]
            else:
                query["fecha"] = {"eq": Data.ini_date.strftime("%Y-%m-%d")}
        if Data.id_state:
            logging.info("Has state(s)")
            logging.debug(f'States: {Data.id_state}')
            for ide in Data.id_state:
                query["id_estado"] = {"eq": ide}
                url = settings.url_citas+'?q='+json.dumps(query)
                logging.debug(f'URL state id: {url}')
                response = requests.get(url, headers=headers)
                if response.status_code != 200:
                    logging.error(response.text)
                    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Error getting appointments"})
                response = json.loads(response.text)
                Appointments = Appointments + response["data"]
            if Data.id_office:
                Appointments = [cita for cita in Appointments if cita["id_sucursal"] in Data.id_office]
        else:
            logging.info("No states")
            url = settings.url_citas+'?q='+json.dumps(query)
            logging.debug(f'URL: {url}')
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                logging.error(response.text)
                return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Error getting appointments"})
            response = json.loads(response.text)
            Appointments = Appointments + response["data"]
        if Data.id_office:
            Appointments = [cita for cita in Appointments if cita["id_sucursal"] in Data.id_office]

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(Appointments))

@router.put("/update_appointment")
async def change_state_appointments(State:StateAppointmentModel = None) -> JSONResponse:
    
    if not State:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "No data provided"})
    logging.info("Changing state of appointment...")
    logging.debug(f'ID appointment: {State.id_appointment}')
    logging.debug(f'ID state: {State.id_state}')
    logging.debug(f'Comments: {State.comments}')
    headers = {
        'Authorization': 'Token ' + settings.app_token
    }
    url = settings.url_citas +'/'+ str(State.id_appointment)
    logging.debug(f'URL: {url}')
    data = {"id_estado": State.id_state, "comentarios": State.comments} if State.comments else {"id_estado": State.id_state}
    logging.debug(f'Data to send: {data}')
    response = requests.put(url, headers=headers, data=data)
    if response.status_code != 200:
        logging.error(response.text)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Error changing state of appointment"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(response.json()))