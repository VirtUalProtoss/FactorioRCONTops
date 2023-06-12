import logging
import sys
from prometheus_client import Gauge
from urllib.error import HTTPError

from rcon_top import get_tops


log = logging.getLogger("logger")


class Metrics():

    def __init__(self, client):
        self.resources_map = {}
        self.labels_map = {
        }
        self.gauges = {}
        self.update_errors_count = 0
        self.client = client

    def update_resources(self):
        pass

    def clear_metrics(self):
        for gauge in self.gauges.values():
            gauge.clear()

    def update_metrics(self):
        tops = get_tops(self.client)
        for top in tops:
            metric_name = top["name"]
            metric_data = top["data"]
            if metric_name not in self.gauges:
                self.gauges[metric_name] = Gauge(
                    metric_name,
                    top["description"],
                    ["nickname", "place", "top_category"]
                )
            for row in metric_data:
                self.gauges[metric_name].labels(
                    row["nickname"],
                    row["place"],
                    row["top_category"],
                ).set(row["value"])

    def refresh_metrics(self):
        self.clear_metrics()
        try:
            self.update_metrics()
            self.update_errors_count = 0
        except HTTPError as e:
            if self.update_errors_count > 2:
                log.error(f'I can not update metrics. Error "{e}". Bye!')
                sys.exit(1)
            self.update_errors_count += 1
            log.info(
                f'#{self.update_errors_count} Update metrics error "{e}".'
                ' I will try to update token and continue'
            )
            self.metrics.cdn._refresh_token()
            self.refresh_metrics()
