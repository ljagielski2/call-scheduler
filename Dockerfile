FROM python:3.6
COPY requirements.txt /src/requirements.txt
RUN pip install --trusted-host pypi.python.org -r src/requirements.txt
COPY server.py /src
COPY sns_sender.py /src
COPY spreadsheet_reader.py /src
COPY credentials.json /src
COPY templates /src/templates
CMD FLASK_APP=server.py flask run
