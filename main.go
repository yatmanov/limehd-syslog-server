package main

import (
	"fmt"
	"gopkg.in/mcuadros/go-syslog.v2"
)

func main() {
	fmt.Println("LimeHD syslog server")

	channel := make(syslog.LogPartsChannel)
	handler := syslog.NewChannelHandler(channel)

	server := syslog.NewServer()
	// RFC5424 - не подходит
	// RFC3164
	server.SetFormat(syslog.RFC3164)
	server.SetHandler(handler)
	server.ListenUDP("0.0.0.0:514")

	server.Boot()

	go func(channel syslog.LogPartsChannel) {
		for logParts := range channel {
			fmt.Println(logParts)
		}
	}(channel)

	server.Wait()
}
