SCRIPT_AUTHOR=Danil Pismenny <danil@brandymint.ru>
SCRIPT_VERSION=0.0.1

all: clean build

build: limehd-syslog-server

clean:
	rm -f limehd-syslog-server

limehd-syslog-server:
	go build 
