package main

import (
	"time"

	"github.com/namjunjeong/Smart-Bollard-System/rasp_servo"
)

func main() {
	servo := rasp_servo.BollardInit(18)
	time.Sleep(time.Second)
	for i := 0; i < 5; i++ {
		rasp_servo.BollardClose(&servo, 10, time.Second*2)
		rasp_servo.BollardOpen(&servo, 20, time.Second*2)
	}
}
