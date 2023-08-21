package main

import (
	"log"
	"time"

	"github.com/stianeikeland/go-rpio/v4"
)

func BollardInit(pinnum int) rpio.Pin {
	servo := rpio.Pin(pinnum)
	servo.Mode(rpio.Pwm)
	servo.Freq(50) //max freq
	servo.DutyCycle(0, 200)
	return servo
}

func BollardOpen(servo *rpio.Pin, sleeptime time.Duration) {
	servo.DutyCycle(6, 200)
	time.Sleep(sleeptime)
}

func BollardClose(servo *rpio.Pin, sleeptime time.Duration) {
	servo.DutyCycle(13, 200)
	time.Sleep(sleeptime)
}

func main() {
	err := rpio.Open()
	if err != nil {
		log.Fatalf("rpio.Open error : %v", err)
	}
	defer rpio.Close()

	servo := BollardInit(18)

	time.Sleep(time.Second)
	for i := 0; i < 5; i++ {
		BollardClose(&servo, time.Second*2)
		BollardOpen(&servo, time.Second*2)
	}
}
