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
	servo.Freq(200) //max freq
	servo.DutyCycle(0, 5)

	for i := uint32(0); i < 5; i++ {
		servo.DutyCycle(i, 5)
		time.Sleep(time.Second)
	}
}
