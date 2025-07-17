package main

import (
	"fmt"
	"net"
	"net/http"
	"github.com/gorilla/websocket"
	"encoding/json"
)

var upgrader = websocket.Upgrader{}
var ports []int

func wsHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Println("Print OK")
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		fmt.Println("Read error: ", err)
	}

	defer conn.Close()
	fmt.Println("Client OK")

	for {
		_, msg, err := conn.ReadMessage()
		if err != nil {
			fmt.Println("Read error: ", err)
		}
		fmt.Printf("Received: %s\n", msg)
	}
}

func find_free_port() (int, error) {
	listener, err := net.Listen("tcp", "localhost:0")
	if err != nil {
		return 0, err
	}
	defer listener.Close()
	return listener.Addr().(*net.TCPAddr).Port, nil
}

func getporthandler(w http.ResponseWriter, r *http.Request) {
	var err error
	var portNew int
	portNew, err = find_free_port()
	if err != nil {
		panic(err)
	}
	fmt.Println(portNew)
	ports = append(ports, portNew)
	response := map[string]int{"port":portNew}
	json.NewEncoder(w).Encode(response)
}

func main() {
	http.HandleFunc("/get-port", getporthandler)

	go func() {
		err := http.ListenAndServe(fmt.Sprintf(":%d", 8080), nil)
		if err != nil {
			panic(err)
		}
	} ()

	go func() {
		for _, port := range(ports) {
			err := http.ListenAndServe(fmt.Sprintf(":%d", port), nil)
			if err != nil {
				panic(err)
			}
			http.HandleFunc("", wsHandler)
		}
	} ()

	select {}

}