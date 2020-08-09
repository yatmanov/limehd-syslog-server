# syslog сервер который собирает статистику с nginx серверов и складывае ее в influxdb

## Installation

1. Python 3.7+ is required (use [pyenv](https://github.com/pyenv/pyenv) or [asdf](https://github.com/asdf-vm/asdf) to install required versions if you need to)

2. Install next libraries to guarantee successful installation of project dependencies:
  ```
    $ sudo apt-get install python3-dev python3-venv build-essential 
  ```
3. Create and activate virtual environment:
  ```
    $ python3 -m venv <your_env_name>
    $ source <your_env_name>/bin/activate
  ```
4. Install dependencies:
  ```
    $ python -m pip install -r requirements.txt
  ```
5. Run server:
  ```
    $ python main.py
  ```

## CLI options

The server takes next cli options:
  - `--port` - порт, который слушает
  - `-i`, `--influx-host`
  - `-d`, `--influx-db`
  - `--mt`
  - `--maxmind`

```
python main.py --port 9999 -i localhost -d 8086 --mt bytes_sent --maxmind /usr/share/GeoIP/GeoLite2-City.mmdb
```

## Боевой сервер

* influx-host: `influx.iptv2022.com`
* database: `polina`

## Метрики

* [ ] Трафик (`value` в measurement `bytes_sent`)
* [ ] online-пользователи (`value` в measurement `connections`)

## Тэги

* `country_id` - ID страны из [maxmind](https://dev.maxmind.com/geoip/legacy/codes/iso3166/)
* `channel`
* `streaming_server`
* `quality`

# Схема

```
+------------------------+                   +-------------------------+
|                        |                   |                         |
|  MEDIA STREAMAING      |   SYSLOG (UDP)    |                         |
|  NGINX SERVERS         |                   |   LIMEHD SYSLOG SERVER  |
|                        |   +----------->   |                         |
+------------------------+                   +-------------------------+
                                                          +
                                                          |
                                                          |
                                                          v
                                              +-----------------------+
                                              |                       |
                                              |        INFLUXDB       |
                                              |                       |
                                              +-----------------------+
```


# Формат

```
29/Apr/2020:21:21:14 +0300|1588184474.870|83.219.236.137|HTTP/1.1|GET|mhd.limehd.tv|/streaming/domashniy/324/vh1w/playlist.m3u8|-|206|4004|0.000|-|-|-|-|-|-|Mozilla/5.0 (Web0S; Linux/SmartTV) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.34 Safari/537.36 WebAppManager|-|1|2313149490
```

Где:

* `vh1w` - `quality`
* `domashniy` - `channel`
* `83.219.236.137` - IP для определения `country_id`
* `mhd.limehd.tv` - `streaming_server`

```
oleg_maksimov  8:25 AM
08:24:43.763016 IP 172.19.95.111.22221 > 194.35.48.67.514: SYSLOG local7.info, length: 527
08:24:43.766297 IP 172.19.95.111.61437 > 194.35.48.67.514: SYSLOG local7.info, length: 356
08:24:43.766326 IP 172.19.95.111.61437 > 194.35.48.67.514: SYSLOG local7.info, length: 295
08:24:43.767118 IP 172.19.95.111.26344 > 194.35.48.67.514: SYSLOG local7.info, length: 470
08:24:43.767415 IP 172.19.95.111.8950 > 194.35.48.67.514: SYSLOG local7.info, length: 452
```


```
log_format csv
                $time_local|
                $msec|
                $remote_addr|
                $server_protocol|
                $request_method|
                $host|
                $uri|
                $args|
                $status|
                $body_bytes_sent|
                $request_time|
                $upstream_response_time|
                $upstream_addr|
                $upstream_status|
                $http_referer|
                $http_via|
                $http_x_forwarded_for|
                $http_user_agent|
                $sent_http_x_profile|
                $connection_requests|
                $connection|
                $bytes_sent;
access_log syslog:server=127.0.0.1:PORT csv;
```
