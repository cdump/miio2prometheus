import time
from dataclasses import dataclass
from typing import Callable, List

import miio
import prometheus_client


@dataclass
class Device:
    cfunc: Callable
    attributes: List[str]
    conn: miio.Device = None

if __name__ == '__main__':
    METRICS_PORT = 5433
    devices = {
        'monitor': Device(
            cfunc=lambda: miio.airqualitymonitor.AirQualityMonitor(ip='192.168.88.100', token='FIXME', model='cgllc.airmonitor.s1'),
            attributes=['battery', 'temperature', 'humidity', 'co2', 'pm25', 'tvoc'],
        ),
        'humidifier': Device(
            cfunc=lambda: miio.airhumidifier.AirHumidifier(ip='192.168.88.101', token='FIXME', model='zhimi.humidifier.ca1'),
            attributes=['temperature', 'humidity', 'target_humidity', 'motor_speed', 'depth'],
        ),
    }

    attributes = {a for _, d in devices.items() for a in d.attributes}
    attributes.add('update_ts')
    metrics = {
        x: prometheus_client.Gauge(f'home_{x}', x, ['device']) for x in attributes
    }

    prometheus_client.start_http_server(METRICS_PORT)
    while True:
        for dname, d in devices.items():
            try:
                if d.conn is None:
                    d.conn = d.cfunc()
                s = d.conn.status()
                print(dname, s)
                for mname in d.attributes:
                    metrics[mname].labels(dname).set(getattr(s, mname))
                metrics['update_ts'].labels(dname).set(int(time.time()))
            except Exception as ex:
                print('Exception:', dname, ex)
                d.conn = None

        time.sleep(1)
