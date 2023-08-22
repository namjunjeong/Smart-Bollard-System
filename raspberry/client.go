package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"os"

	pb "github.com/namjunjeong/Smart-Bollard-System/rasp_proto"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func main() {
	var data = pb.Req{Request: 1}

	conn, err := grpc.Dial(os.Getenv("SERVERADDR"), grpc.WithTransportCredentials(insecure.NewCredentials()))
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
		}
		fmt.Printf("%t\n", res.GetResponse())
	}

}
