package servo

import (
	"log"
	"time"

	"github.com/stianeikeland/go-rpio/v4"
)

func RpioInit() {
	err := rpio.Open()
	if err != nil {
		log.Fatalf("rpio.Open error : %v", err)
	}
	defer rpio.Close()
}

func BollardInit(pinnum int) rpio.Pin {
	servo := rpio.Pin(pinnum)
	servo.Mode(rpio.Pwm)
	servo.Freq(50) //max freq
	servo.DutyCycle(0, 200)
	return servo
}

func BollardOpen(servo *rpio.Pin, dutylen uint32, sleeptime time.Duration) {
	servo.DutyCycle(dutylen, 200)
	time.Sleep(sleeptime)
}

func BollardClose(servo *rpio.Pin, dutylen uint32, sleeptime time.Duration) {
	servo.DutyCycle(dutylen, 200)
	time.Sleep(sleeptime)
}

/*
 */
