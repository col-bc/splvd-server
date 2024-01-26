# SPLVD API

## Description
This FastAPI project contains the endpoints for the SPLVD project. The endpoints are used to retrieve data from the database and to add data to the database. The endpoints are used by the [SPLVD frontend]().

## Installation
### Prerequisites
- Python 3.10+
- pip

### Virtual environment
It is recommended to use a virtual environment to run the project. To create a virtual environment, run the following command:
```bash
python3 -m venv venv
```
Then activate the virtual environment:
```bash
source venv/bin/activate
```

### Install dependencies
With the virtual environment activated, install the dependencies from the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

## Development server
To run the development server, run the following command:
```bash
uvicorn main:app
```
The development server will run on `http://127.0.0.1:8000/`. The interactive API documentation can be found at `http://127.0.0.1:8000/docs`.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contact
- [Github Repository]() - Submit issues and pull requests here
- [Colby Cooper](mailto:colby.b.cooper@gmail.com)