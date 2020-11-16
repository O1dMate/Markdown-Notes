# Using netsh

### Show Cached Wifi Passwords
```bash
netsh wlan show profiles
```

### Show connection status of network interfaces
```bash
netsh interface ipv4 show interfaces
```

### Show IP Address of all Interfaces
```bash
netsh interface ipv4 show ipaddresses
```

### Show Information for All Interfaces (IP, Gateway, Subnet)
```bash
netsh interfaces ipv4 show addresses
```

### Show Network Routing Table
```bash
netsh interface ipv4 show route
```

### Show DNS Servers for Network Interfaces
```bash
netsh interfaces ipv4 show dnsservers
```

### Show Cached IPs of known Hosts on all Interfaces
```bash
netsh interface ipv4 show neighbors
```

### Show Current TCP Connection (Listening & Established)
```bash
netsh interfaces ipv4 show tcpconnections
```

### Show Firewall Status
```bash
netsh advfirewall show allprofiles
```