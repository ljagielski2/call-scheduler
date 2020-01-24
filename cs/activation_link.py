from itsdangerous import URLSafeSerializer, BadSignature
from flask import url_for

from cs import APP

def get_activation_link(employee_idx):
    serializer = URLSafeSerializer(APP.secret_key)
    payload = serializer.dumps(employee_idx)

    with APP.app_context():
        return url_for('shifts', payload=payload, _external=True)

def get_payload(payload):
    serializer = URLSafeSerializer(APP.secret_key)
    employee_num = serializer.loads(payload)
    return employee_num
