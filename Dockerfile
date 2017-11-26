FROM alpine:3.5
RUN apk add --update python py-pip
COPY requirements.txt /src/requirements.txt
RUN pip --cert /etc/ssl/certs/DigiCert_High_Assurance_EV_Root_CA.pem install -r src/requirements.txt
COPY server.py /src
COPY sns_sender.py /src
COPY spreadsheet_reader.py /src
COPY credentials.json /src
COPY templates /src/templates
COPY buzz /src/buzz
CMD FLASK_APP=server.py flask run
