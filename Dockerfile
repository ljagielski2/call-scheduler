FROM python:3.6
COPY requirements.txt /src/requirements.txt
WORKDIR /src
RUN pip install --trusted-host pypi.python.org -r requirements.txt
COPY . /src
EXPOSE 5000
RUN chmod 777 setup.sh
ENTRYPOINT [ "bash" ]
CMD [ "./setup.sh" ]
