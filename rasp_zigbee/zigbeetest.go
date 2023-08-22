package main

import (
	"fmt"
	"log"
	"sync"

	"go.bug.st/serial"
)

func main() {
	var sendmsg string
	var recvmsg string
	var bytemsg []byte
	var wg sync.WaitGroup
	buff := make([]byte, 100)

	mode := &serial.Mode{
		BaudRate: 9600,
	}
	port, err := serial.Open("/dev/ttyUSB0", mode)
	if err != nil {
		log.Fatalf("serial.Open error : %v", err)
	}
	
	wg.Add(2)
	go func(){
		defer wg.Done()
		for{
			fmt.Scanln(&sendmsg)
			bytemsg = []byte(sendmsg)
			_, err := port.Write(bytemsg)
			if err != nil {
				log.Fatal(err)
				break
			}
			if sendmsg == "quit"{
				break
			}
		}
		fmt.Println("sender done")
	}()

	go func(){
		defer wg.Done()
		for{
			n,err:=port.Read(buff)
			if err != nil{
				log.Fatal(err)
				break
			}
			if n==0{
				fmt.Println("\nEOF")
				break
			}
			recvmsg = string(buff[:n])
			if recvmsg == "quit"{
				break
			}
			fmt.Println(recvmsg)
		}
		fmt.Println("receiver done")
	}()
	wg.Wait()
}
