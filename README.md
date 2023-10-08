## Usage examples
### Start/stop socks server
```bash
#by default targets 127.0.0.1:1080
fwdctrl socks add
fwdctrl socks rm
#custom host:port
fwdctrl socks add -l 127.0.0.1:1090
fwdctrl socks rm -l 127.0.0.1:1090
```

### Start/stop reverse port forwarding
```bash
fwdctrl reverse add -l 127.0.0.1:8445 -r 127.0.0.1:8445
fwdctrl reverse rm -l 127.0.0.1:8445 -r 127.0.0.1:8445
```

### List configured endpoints
```bash
fwdctrl list
```

### List files
```bash
fwdctrl ls .
fwdctrl ls '/c:/'
```

### List files by mask
```bash
fwdctrl glob '/c:/*.dll'
```

### Download a file
```bash
fwdctrl get '/c:/my_file.exe'
```

### Download files by mask
```bash
fwdctrl get_glob '/c:/*.dll'
```
