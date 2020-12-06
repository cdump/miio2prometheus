# miio2prometheus

Пример экспорта измерений с устройств Xiaomi в [prometheus](https://prometheus.io/)
- Монитор качества воздуха Xiaomi Cleargrass CGS1
- Увлажнитель воздуха Xiaomi Smartmi Zhimi Air Humidifier 2


Получить токены устройств (чтобы заменить `FIXME` в скрипте): [инструкция](https://github.com/jghaanstra/com.xiaomi-miio/blob/master/docs/obtain_token.md)

## Запуск
- Установить [python poetry](https://python-poetry.org/)
- Выполнить
```sh
$ git clone https://github.com/cdump/miio2prometheus.git
$ cd miio2prometheus
$ poetry install
$ poetry run python3 miio2prometheus.py
```
- Метрики доступы на `http://127.0.0.1:5433/metrics`
