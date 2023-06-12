import os
import logging
import sys
from config import settings
from http.server import HTTPServer
from metrics import Metrics
from prometheus_client import MetricsHandler
import factorio_rcon


RCON_ADDR = os.environ.get("RCON_ADDR", "127.0.0.1")
RCON_PORT = os.environ.get("RCON_PORT", "27015")
RCON_PASS = os.environ.get("RCON_PASS", "123")

log = logging.getLogger("logger")
log.setLevel(settings.get("LOGLEVEL", "INFO"))
log.addHandler(logging.StreamHandler(sys.stderr))


class HttpHandler(MetricsHandler):

    try:
        client = factorio_rcon.RCONClient(
            RCON_ADDR, int(RCON_PORT), RCON_PASS
        )
        metrics = Metrics(client)
    except Exception as e:
        log.error("Metrics initialization failed")
        raise e

    def do_GET(self):
        if self.path == "/metrics":
            self.metrics.refresh_metrics()
            super().do_GET()
        else:
            self.send_error(404)


if __name__ == "__main__":
    log.info(f"Starting web server at port {settings.get('WEB_PORT', 8090)}")
    HTTPServer(
        ("0.0.0.0", settings.get("WEB_PORT", 8090)),
        HttpHandler
    ).serve_forever()
