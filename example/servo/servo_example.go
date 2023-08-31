package main

import (
	"time"

	"github.com/namjunjeong/Smart-Bollard-System/rasp_servo"
)

func main() {
	rasp_servo.RpioInit()
	defer rasp_servo.RpioClose()
	servo := rasp_servo.BollardInit(18)
	time.Sleep(time.Second)
	for i := 0; i < 5; i++ {
		rasp_servo.BollardControl(servo, 10, time.Second*2)
		rasp_servo.BollardControl(servo, 20, time.Second*2)
	}
}
