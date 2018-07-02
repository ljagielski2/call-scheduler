FROM python:3.6
COPY requirements.txt /src/requirements.txt
RUN pip install --trusted-host pypi.python.org -r src/requirements.txt
COPY server.py server.py
COPY sns.py sns.py
COPY spreadsheet_reader.py spreadsheet_reader.py
COPY credentials.json credentials.json
COPY templates templates
COPY tests tests
CMD python server.py
