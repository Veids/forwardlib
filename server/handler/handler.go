package handler

import (
	"io"
	"log"
	"net"
	"net/rpc"
	"sync"

	"github.com/Veids/forwardlib/common"
	rrpc "github.com/Veids/forwardlib/server/rpc"

	"github.com/hashicorp/yamux"
	"github.com/pkg/sftp"
	"github.com/things-go/go-socks5"
)

type Control struct {
	sync.RWMutex
	stream          *net.Conn
	serverRpcServer *rrpc.ServerRpcServer
}

type Handler struct {
	server  *socks5.Server
	control Control
	session *yamux.Session
	sftp    *sftp.Server
}

func (s *Handler) HandleStream(stream net.Conn) {
	//TODO: Handle read size
	stype := make([]byte, 1)
	stream.Read(stype)

	switch stype[0] {
	case common.CONTROL:
		s.control.Lock()
		if s.control.stream != nil {
			log.Println("Control stream already defined")
		} else {
			s.control.stream = &stream
			s.control.serverRpcServer = rrpc.NewServerRpcServer(s.session)
			r := rpc.NewServer()
			r.Register(s.control.serverRpcServer)
			go r.ServeConn(stream)
		}
		s.control.Unlock()
		break
	case common.SOCKS:
		log.Println("Passing off to socks5")
		go func() {
			err := s.server.ServeConn(stream)
			if err != nil {
				log.Println(err)
			}
		}()
		break
	case common.PORT_FORWARD:
		log.Println("Passing off to Forward")
		var addr common.Addr
		addr.Unmarshal(stream)
		remoteAddr := addr.ToString()

		go func() {
			tcpAddr, err := net.ResolveTCPAddr("tcp", remoteAddr)
			if err != nil {
				log.Printf("Failed to resolve forward addr: %v", err)
				stream.Close()
				return
			}

			conn, err := net.DialTCP("tcp", nil, tcpAddr)
			if err != nil {
				log.Printf("Failed to establish reverse tcp connection: %s", err)
				stream.Close()
				return
			}

			go func() {
				log.Printf("Starting to copy conn to stream for %s", conn.RemoteAddr())
				io.Copy(conn, stream)
				conn.Close()
				log.Printf("Done copying conn to stream for %s", conn.RemoteAddr())
			}()

			go func() {
				log.Printf("Starting to copy stream to conn for %s", conn.RemoteAddr())
				io.Copy(stream, conn)
				stream.Close()
				log.Printf("Done copying stream to conn for %s", conn.RemoteAddr())
			}()
		}()
	case common.SFTP:
		log.Println("Passing off to SFTP")
		go func() {
			options := []sftp.ServerOption{}

			server, err := sftp.NewServer(stream, options...)
			if err != nil {
				panic(err)
			}

			if err := server.Serve(); err == io.EOF {
				server.Close()
				log.Print("sftp client exited session.")
			} else if err != nil {
				panic(err)
			}
		}()
	default:
		log.Printf("Invalid stream type %d", stype[0])
		stream.Close()
	}
}

func Loop(conn io.ReadWriteCloser) {
	session, err := yamux.Server(conn, nil)
	if err != nil {
		panic(err)
	}
	handler := Handler{
		server:  socks5.NewServer(),
		session: session,
	}

	for {
		stream, err := session.Accept()
		if err != nil {
			panic(err)
		}
		log.Println("Stream accepted")
		handler.HandleStream(stream)
	}
}
