SCRIPT_AUTHOR=Danil Pismenny <danil@brandymint.ru>
SCRIPT_VERSION=0.0.1
HOST=rz.iptv2022.com

all: clean build

build: limehd-syslog-server

clean:
	rm -f limehd-syslog-server

deploy:
	scp limehd-syslog-server root@${HOST}:/root/

limehd-syslog-server:
	go build 

shell:
	ssh root@rz.iptv2022.com
