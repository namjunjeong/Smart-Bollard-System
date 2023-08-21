package main

import (
	"log"
	"time"
	"fmt"
	"github.com/stianeikeland/go-rpio/v4"
)

func main() {
	err := rpio.Open()
	if err != nil {
		log.Fatalf("rpio.Open error : %v", err)
	}
	defer rpio.Close()
	
	fmt.Println("setting start")
	servo := rpio.Pin(18)
	servo.Mode(rpio.Pwm)
	servo.Freq(50) //max freq
	servo.DutyCycle(0, 200)
	fmt.Println("setting finish")
	time.Sleep(time.Second*3)
	for i := 0; i<5; i++ {
		fmt.Println("start loop")
		for i := uint32(0); i < 200; i++ {
			servo.DutyCycle(i, 200)
			time.Sleep(time.Second/32)
		}
		for i := uint32(200); i > 0; i-- {
			servo.DutyCycle(i, 200)
			time.Sleep(time.Second/32)
		}
		fmt.Println("end loop")
		time.Sleep(time.Second)
	}
}
