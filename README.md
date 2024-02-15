# Cero Dentalink API

For the Cero Dentalink API, we use the following technologies:
- Python 3.11
- FastAPI
- Docker

## Installation

To install the project, you need to have Docker installed on your machine. Then, you can run the following command:

```bash
docker-compose up -d --build
```

## Usage

To use the project, you can access the following URL to test the API:

```bash
http://localhost:8000/docs
```

Also you can test the API using postman or any other tool. The base URL is:

```bash
http://localhost:8000/appointments
```

### Get Appointments
To get the list of appointments, you can use the following URL:

```bash
http://localhost:8000/appointments/get_appointments
```
the search parameters are:
- ini_date: Initial date to search or the especific date to search (format: YYYY-MM-DD) **optional**
- end_date: Final date to search (format: YYYY-MM-DD) **optional**
- id_state (list[int]): List of state ids to search **optional**
- id_office (list[int]): List of office ids to search **optional**

### Update Appointment
To update an appointment, you can use the following URL:

```bash
http://localhost:8000/appointments/update_appointment
```
the parameters are:
- id_appointment (int): Appointment id to update **required**
- id_state (int): State id to update **required**
- comment (str): Comment to update **optional**