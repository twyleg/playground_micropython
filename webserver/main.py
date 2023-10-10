import json
import logging
import sys
import time
from wifi import connect, read_connection_details_from_file
from picoweb import WebApp, start_response


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

connected_wifi = connect(*read_connection_details_from_file())
my_address = connected_wifi.ifconfig()[0]

app = WebApp(__name__)


@app.route("/time")
def time_get(req, resp):
    req.parse_qs()

    now = time.time()
    json_str = json.dumps({"time": now})

    yield from start_response(resp, status=200, content_type="text/json")
    yield from resp.awrite(json_str.encode())


app.run(debug=True, host=my_address, port=8080, lazy_init=False, log=logging.getLogger())