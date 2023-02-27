from chalice import Chalice
import json

from chalicelib.db import db

app = Chalice(app_name="ingest")


@app.on_sqs_message(queue="wikipedia", batch_size=1)
def handler(event):
    for record in event:
        body = json.loads(record.to_dict().get("body"))
        for key, value in body.items():
            db.put(project=key, articles=value)
