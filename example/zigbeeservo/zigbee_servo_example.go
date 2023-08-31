package main

import (
	"fmt"
	"log"
	"sync"
	"time"

	"github.com/namjunjeong/Smart-Bollard-System/rasp_servo"
	"github.com/namjunjeong/Smart-Bollard-System/rasp_zigbee"
)

func main() {
	rasp_servo.RpioInit()
	defer rasp_servo.RpioClose()
	servo := rasp_servo.BollardInit(18)

	var sendmsg string
	var recvmsg string
	var bytemsg []byte
	var wg sync.WaitGroup
	buff := make([]byte, 100)
	port := rasp_zigbee.OpenSerial("/dev/ttyUSB0", 9600)

	wg.Add(2)
	go func() {
		defer wg.Done()
		for {
			fmt.Scanln(&sendmsg)
			bytemsg = []byte(sendmsg)
			_, err := port.Write(bytemsg)
			if err != nil {
				log.Fatal(err)
				break
			}
			if sendmsg == "quit" {
				break
			} else if sendmsg == "o" {
				rasp_servo.BollardControl(servo, 10, time.Second)
			} else if sendmsg == "c" {
				rasp_servo.BollardControl(servo, 20, time.Second)
			}
		}
		fmt.Println("sender done")
	}()

	go func() {
		defer wg.Done()
		for {
			n, err := port.Read(buff)
			if err != nil {
				log.Fatal(err)
				break
			}
			if n == 0 {
				fmt.Println("\nEOF")
				break
			}
			recvmsg = string(buff[:n])
			if recvmsg == "quit" {
				break
			}
			fmt.Println(recvmsg)
		}
		fmt.Println("receiver done")
	}()
	wg.Wait()
}
