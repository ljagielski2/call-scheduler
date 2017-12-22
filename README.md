# call-scheduler
[![Build Status](https://travis-ci.org/ljagielski2/call-scheduler.svg?branch=master)](https://travis-ci.org/ljagielski2/call-scheduler)

A webapp that allows employees to choose their call shifts by seniority. On startup, a background process is scheduled to send a text message to the next employee on a certain interval. The text message contains a personalized link to the scheduling webapp. Employees can then choose their shift, or choose to give their shift to another employee.

## Run Steps

Clone the project to your local:

```
git clone https://github.com/ljagielski2/call-scheduler.git
```

Install dependencies from your terminal:

```
pip install -r requirements.txt
```

Start the server:

```
python server.py
```
