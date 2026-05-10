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
	if err != nil {
		panic(err)
	}
	cstream.Write([]byte{common.CONTROL})

	control := rpc.NewClient(cstream)
	reverse := handlers.NewReverseHandler(session)
	go reverse.Serve()

	var sftpClient *sftp.Client
	sftpStream, err := session.Open()
	if err != nil {
		log.Printf("SFTP unavailable: failed to open stream: %v", err)
	} else {
		_, err = sftpStream.Write([]byte{common.SFTP})
		if err != nil {
			log.Printf("SFTP unavailable: failed to select stream type: %v", err)
			sftpStream.Close()
		} else {
			sftpClient, err = sftp.NewClientPipe(sftpStream, sftpStream)
			if err != nil {
				log.Printf("SFTP unavailable: %v", err)
				sftpStream.Close()
			}
		}
	}

	s := handlers.NewClientRpcServer(session, control, &reverse, sftpClient)

	var opts []grpc.ServerOption
	grpcServer := grpc.NewServer(opts...)
	clientpb.RegisterClientRpcServer(grpcServer, s)
	grpcServer.Serve(lis)
}
