package main

import (
	"log"
	"time"

	"github.com/stianeikeland/go-rpio/v4"
)

func main() {
	err := rpio.Open()
	if err != nil {
		log.Fatalf("rpio.Open error : %v", err)
	}
	defer rpio.Close()

	servo := rpio.Pin(18)
	servo.Mode(rpio.Pwm)
	servo.Freq(50) //max freq
	servo.DutyCycle(0, 200)
	time.Sleep(time.Second)
	for i := 0; i < 5; i++ {
		servo.DutyCycle(0,200)
		time.Sleep(time.Second * 2)
		servo.DutyCycle(6,200)
		time.Sleep(time.Second * 2)
		servo.DutyCycle(13,200)
		time.Sleep(time.Second * 2)
		servo.DutyCycle(6,200)
		time.Sleep(time.Second * 2)
	}
}
