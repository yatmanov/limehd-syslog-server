# Схема

https://docs.google.com/drawings/d/15qWcQgiTo16clO7jfKQyXk9UJABi434Q_Ey0dY-PYy8/edit


# Формат

```
29/Apr/2020:21:21:14 +0300|1588184474.870|83.219.236.137|HTTP/1.1|GET|mhd.limehd.tv|/streaming/domashniy/324/vh1w/playlist.m3u8|-|206|4004|0.000|-|-|-|-|-|-|Mozilla/5.0 (Web0S; Linux/SmartTV) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.34 Safari/537.36 WebAppManager|-|1|2313149490
```

```

oleg_maksimov  8:25 AM
08:24:43.763016 IP 172.19.95.111.22221 > 194.35.48.67.514: SYSLOG local7.info, length: 527
08:24:43.766297 IP 172.19.95.111.61437 > 194.35.48.67.514: SYSLOG local7.info, length: 356
08:24:43.766326 IP 172.19.95.111.61437 > 194.35.48.67.514: SYSLOG local7.info, length: 295
08:24:43.767118 IP 172.19.95.111.26344 > 194.35.48.67.514: SYSLOG local7.info, length: 470
08:24:43.767415 IP 172.19.95.111.8950 > 194.35.48.67.514: SYSLOG local7.info, length: 452





8:29
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
```
