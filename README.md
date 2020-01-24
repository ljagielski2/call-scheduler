# call-scheduler
[![Build Status](https://travis-ci.org/ljagielski2/call-scheduler.svg?branch=master)](https://travis-ci.org/ljagielski2/call-scheduler)

A webapp that allows employees to choose their call shifts by seniority. On startup, a background process is scheduled to send a text message to the next employee on a certain interval. The text message contains a personalized link to the scheduling webapp. Employees can then choose their shift, or choose to give their shift to another employee.

## Run Steps

Clone the project to your local:

```
git clone https://github.com/ljagielski2/call-scheduler.git
```

Build docker container:

```
docker build -t call-scheduler:latest .
```

Start the server:

```
docker run -d -p 5000:5000 call-scheduler:latest
```

Visit http://0.0.0.0:5000/admin in your browser
