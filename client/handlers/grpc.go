package handlers

import (
	"fmt"
	"io"
	"log"
	"net"
	"net/rpc"
	"os"
	"path/filepath"

	"github.com/Veids/forwardlib/common"
	clientpb "github.com/Veids/forwardlib/protobuf/clientpb"
	commonpb "github.com/Veids/forwardlib/protobuf/commonpb"
	"github.com/pkg/sftp"

	"github.com/hashicorp/yamux"
	"golang.org/x/net/context"
)

type ClientRpcServer struct {
	session *yamux.Session
	socks   SocksServers
	reverse *ReverseHandler
	forward ForwardServers
	control *rpc.Client
	sftp    *sftp.Client
	clientpb.UnimplementedClientRpcServer
}

func NewClientRpcServer(session *yamux.Session, control *rpc.Client, reverse *ReverseHandler, sftp *sftp.Client) *ClientRpcServer {
	return &ClientRpcServer{
		session,
		SocksServers{m: make(map[string]*SocksServer)},
		reverse,
		ForwardServers{m: make(map[string]*ForwardServer)},
		control,
		sftp,
		clientpb.UnimplementedClientRpcServer{},
	}
}

func (s *ClientRpcServer) SocksStart(ctx context.Context, addr *commonpb.Addr) (*commonpb.Empty, error) {
	address := fmt.Sprintf("%s:%d", addr.Ip, addr.Port)
	s.socks.Lock()
	defer s.socks.Unlock()

	if _, ok := s.socks.m[address]; ok {
		return nil, fmt.Errorf("Socks listener %s already exist", address)
	} else {
		l, err := net.Listen("tcp", address)
		if err != nil {
			return nil, err
		}
		v := &SocksServer{
			listener: l,
			quit:     make(chan interface{}),
			session:  s.session,
		}
		v.wg.Add(1)
		s.socks.m[address] = v
		go v.Serve()
		log.Printf("Started socks server on %s:%d\n", addr.Ip, addr.Port)
		return &commonpb.Empty{}, nil
	}
}

func (s *ClientRpcServer) SocksStop(ctx context.Context, addr *commonpb.Addr) (*commonpb.Empty, error) {
	address := fmt.Sprintf("%s:%d", addr.Ip, addr.Port)
	s.socks.Lock()
	defer s.socks.Unlock()

	if val, ok := s.socks.m[address]; ok {
		val.Stop()
		delete(s.socks.m, address)
	} else {
		return nil, fmt.Errorf("Socks listener %s doesn't exist", address)
	}
	return &commonpb.Empty{}, nil
}

func (s *ClientRpcServer) ReverseStart(ctx context.Context, addrPack *commonpb.AddrPack) (*commonpb.Empty, error) {
	local_address := fmt.Sprintf("%s:%d", addrPack.Local.Ip, addrPack.Local.Port)
	remote_address := fmt.Sprintf("%s:%d", addrPack.Remote.Ip, addrPack.Remote.Port)

	s.reverse.dictionary.Lock()
	defer s.reverse.dictionary.Unlock()

	if _, ok := s.reverse.dictionary.m[remote_address]; ok {
		return nil, fmt.Errorf("Reverse listener %s already exist", remote_address)
	} else {
		s.reverse.dictionary.m[remote_address] = &local_address
		log.Printf("Added reverse handler %s", remote_address)
	}

	var reply string
	err := s.control.Call("ServerRpcServer.ReverseStart", common.Addr{
		Ip:   addrPack.Remote.Ip,
		Port: addrPack.Remote.Port,
	}, &reply)

	if err != nil {
		delete(s.reverse.dictionary.m, remote_address)
		return &commonpb.Empty{}, err
	}

	return &commonpb.Empty{}, nil
}

func (s *ClientRpcServer) ReverseStop(ctx context.Context, remoteAddr *commonpb.Addr) (*commonpb.Empty, error) {
	remote_address := fmt.Sprintf("%s:%d", remoteAddr.Ip, remoteAddr.Port)

	s.reverse.dictionary.Lock()
	defer s.reverse.dictionary.Unlock()

	if _, ok := s.reverse.dictionary.m[remote_address]; ok {
		var reply string
		err := s.control.Call("ServerRpcServer.ReverseStop", common.Addr{
			Ip:   remoteAddr.Ip,
			Port: remoteAddr.Port,
		}, &reply)
		if err != nil {
			log.Printf("Failed to stop reverse handler on the server: %s %v", reply, err)
		}

		delete(s.reverse.dictionary.m, remote_address)
		log.Printf("Removed reverse handler %s", remote_address)
	} else {
		return nil, fmt.Errorf("Reverse listener %s doesn't exist", remote_address)
	}

	return &commonpb.Empty{}, nil
}

func (s *ClientRpcServer) List(ctx context.Context, _ *commonpb.Empty) (*clientpb.EndpointList, error) {
	list := clientpb.EndpointList{}

	s.socks.RLock()
	for k := range s.socks.m {
		list.Endpoints = append(list.Endpoints, fmt.Sprintf("socks5 %s", k))
	}
	s.socks.RUnlock()

	s.reverse.dictionary.Lock()
	for k, v := range s.reverse.dictionary.m {
		list.Endpoints = append(list.Endpoints, fmt.Sprintf("reverse %s %s", *v, k))
	}
	s.reverse.dictionary.Unlock()

	s.forward.RLock()
	for k, v := range s.forward.m {
		list.Endpoints = append(list.Endpoints, fmt.Sprintf("forward %s %s:%d", k, v.remote_address.Ip, v.remote_address.Port))
	}
	s.forward.RUnlock()

	return &list, nil
}

func (s *ClientRpcServer) ListFiles(ctx context.Context, path *clientpb.Path) (*clientpb.FileList, error) {
	fileList := clientpb.FileList{}

	fInfo, err := s.sftp.ReadDir(path.Path)

	if err != nil {
		return nil, err
	}

	for _, s := range fInfo {
		fileList.Files = append(fileList.Files, s.Name())
	}

	return &fileList, nil
}

func (s *ClientRpcServer) Glob(ctx context.Context, path *clientpb.Path) (*clientpb.FileList, error) {
	fInfo, err := s.sftp.Glob(path.Path)
	if err != nil {
		return nil, err
	}

	fileList := clientpb.FileList{}
	fileList.Files = fInfo

	return &fileList, nil
}

func (s *ClientRpcServer) Download(ctx context.Context, req *clientpb.DownloadRequest) (*commonpb.Empty, error) {
	source, err := s.sftp.Open(req.Input.Path)
	if err != nil {
		return nil, err
	}
	defer source.Close()

	log.Printf("Downloading: %s", source.Name())
	outName := filepath.Join(req.Output.Path, filepath.Base(source.Name()))
	dest, err := os.Create(outName)
	if err != nil {
		return nil, err
	}
	defer dest.Close()

	nBytes, err := io.Copy(dest, source)
	if err != nil {
		return nil, err
	}
	log.Printf("Transfered: %d", nBytes)

	return &commonpb.Empty{}, nil
}

func (s *ClientRpcServer) ForwardStart(ctx context.Context, addrPack *commonpb.AddrPack) (*commonpb.Empty, error) {
	local_address := fmt.Sprintf("%s:%d", addrPack.Local.Ip, addrPack.Local.Port)

	s.forward.Lock()
	defer s.forward.Unlock()

	if _, ok := s.forward.m[local_address]; ok {
		return nil, fmt.Errorf("Forward listener %s already exist", local_address)
	} else {
		l, err := net.Listen("tcp", local_address)
		if err != nil {
			return nil, err
		}
		v := &ForwardServer{
			listener: l,
			quit:     make(chan interface{}),
			session:  s.session,
			remote_address: common.Addr{
				Ip:   addrPack.Remote.Ip,
				Port: addrPack.Remote.Port,
			},
		}
		v.wg.Add(1)
		s.forward.m[local_address] = v
		go v.Serve()
		log.Printf("Started forward server on %s\n", local_address)
		return &commonpb.Empty{}, nil
	}
}

func (s *ClientRpcServer) ForwardStop(ctx context.Context, localAddr *commonpb.Addr) (*commonpb.Empty, error) {
	address := fmt.Sprintf("%s:%d", localAddr.Ip, localAddr.Port)
	s.forward.Lock()
	defer s.forward.Unlock()

	if val, ok := s.forward.m[address]; ok {
		val.Stop()
		delete(s.forward.m, address)
	} else {
		return nil, fmt.Errorf("Forward listener %s doesn't exist", address)
	}
	return &commonpb.Empty{}, nil
}
