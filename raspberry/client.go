package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"os"
	"time"

	"github.com/joho/godotenv"
	pb "github.com/namjunjeong/Smart-Bollard-System/rasp_proto"

	"github.com/namjunjeong/Smart-Bollard-System/rasp_servo"
	"github.com/namjunjeong/Smart-Bollard-System/rasp_zigbee"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func main() {
	var data = pb.Req{Request: 0}
	var curbollard = false
	var bollard_oc = []byte("oc")

	err := godotenv.Load(".env")
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	rasp_servo.RpioInit()
	defer rasp_servo.RpioClose()
	servo := rasp_servo.BollardInit(18)
	time.Sleep(time.Second)

	port := rasp_zigbee.OpenSerial("/dev/ttyUSB0", 9600)

	conn, err := grpc.Dial(os.Getenv("GRPCSERVERADDR"), grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("connection error : %v", err)
	}
	defer conn.Close()

	client := pb.NewResultClient(conn)

	stream, err := client.Require(context.Background(), &data)
	if err != nil {
		log.Fatalf("request failed : %v", err)
	}
	fmt.Println("request finish")

	for {
		res, err := stream.Recv()

		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatalf("can't receive : %v", err)
			break
		}
		if res.GetResponse() && !curbollard {
			curbollard = !curbollard
			port.Write(bollard_oc[0:1])
			rasp_servo.BollardOpen(servo, 10, time.Second)
		} else if !res.GetResponse() && curbollard {
			curbollard = !curbollard
			port.Write(bollard_oc[1:2])
			rasp_servo.BollardOpen(servo, 20, time.Second)
		}
	}

}
