package main

import "time"

func main() {
	servo := BollardInit(18)
	time.Sleep(time.Second)
	for i := 0; i < 5; i++ {
		BollardClose(&servo, time.Second*2)
		BollardOpen(&servo, time.Second*2)
	}
}
