package handler

import (
	"io"
	"log"
	"net"
	"net/rpc"

	"github.com/Veids/forwardlib/client/handlers"
	"github.com/Veids/forwardlib/common"
	"github.com/Veids/forwardlib/protobuf/clientpb"
	"github.com/pkg/sftp"

	"github.com/hashicorp/yamux"
	"google.golang.org/grpc"
)

func Loop(conn io.ReadWriteCloser, controlAddr string) {
	session, err := yamux.Client(conn, nil)
	if err != nil {
		log.Printf("Error creating client in yamux")
		panic(err)
	}

	lis, err := net.Listen("tcp", controlAddr)
	if err != nil {
		panic(err)
	}

	cstream, err := session.Open()
	cstream.Write([]byte{common.CONTROL})
	if err != nil {
		panic(err)
	}

	control := rpc.NewClient(cstream)
	reverse := handlers.NewReverseHandler(session)
	go reverse.Serve()

	sftpStream, err := session.Open()
	if err != nil {
		panic(err)
	}
	sftpStream.Write([]byte{common.SFTP})

	sftp, err := sftp.NewClientPipe(sftpStream, sftpStream)
	if err != nil {
		panic(err)
	}

	s := handlers.NewClientRpcServer(session, control, &reverse, sftp)

	var opts []grpc.ServerOption
	grpcServer := grpc.NewServer(opts...)
	clientpb.RegisterClientRpcServer(grpcServer, s)
	grpcServer.Serve(lis)
}
