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
	time.Sleep(time.Second)
	for i := 0; i<5; i++ {
		servo.DutyCycle(10,200)
		time.Sleep(time.Second*2)
		servo.DutyCycle(16,200)
		time.Sleep(time.Second*2)
		servo.DutyCycle(10,200)
		time.Sleep(time.Second*2)
		servo.DutyCycle(16,200)
		time.Sleep(time.Second*2)
		fmt.Println("end loop")
	}
}
