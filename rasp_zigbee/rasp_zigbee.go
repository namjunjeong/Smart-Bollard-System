package rasp_zigbee

import (
	"log"

	"go.bug.st/serial"
)

func OpenSerial(portName string, BR int) serial.Port {
	mode := &serial.Mode{
		BaudRate: BR,
	}
	port, err := serial.Open("/dev/ttyUSB0", mode)
	if err != nil {
		log.Fatalf("serial.Open error : %v", err)
	}
	return port
}
