# Linux Networking

### Network Interfaces
 - View Network Interfaces
```bash
ip a
```

 - View Detailed Interface Data
```bash
ip a list [INTERFACE]
```
 - Example
```bash
ip a list eth0
```

 - View Interface State
```bash
ip link
```

 - Change Interface State
```bash
ip link set dev [INTERFACE] up/down
```
 - Example
```bash
ip link set dev eth0 down
```





### Assign IP Address to an Interface
 - Assign IP
```bash
ip a add [ADDRESS/MASK] dev [INTERFACE]
``` 
 - Example
```bash
ip a add 192.168.1.200/24 dev eth0
```

 - Delete assigned IP
```bash
ip a delete [ADDRESS/MASK] dev [INTERFACE]
``` 





### Display Routing Table
```bash
ip route
```




### Settiing up Static Network Credentials
 - Open the file /etc/network/interfaces
 - Add the following
```bash
adddress 192.168.2.19
netmask 255.255.255.0
network 192.168.2.0
broadcast 192.168.2.255
```
 - In the terminal, run the following:
```bash
ip route add 192.168.2.0/24 dev eth0
route add default gateway 192.168.2.1 eth0
```




### Forwarding Using IP Tables
 - List all the rules for the selected chain. If no chain is giving, all are shown
```bash
iptables -L
```

 - Display the chains for the NAT table
```bash
iptables -t nat -L 
```

 - Flush the NAT table and remove all routing commands
```bash
iptables -t nat -L -flush
```


 - Create a new route to forward traffic
```bash
iptables -t [TABLE_NAME] -A [CHAIN_NAME] -p [PROTOCOL] -destination-port [DST_PORT] -j [EXTENSION] -to-port [TO_PORT]
```
 - `-t` specifies which table to add the rule to
 - `-A` specifies which chain in the table the rule is to be added to
 - `-p` specifies which protocol to use
 - `-destination-port` is the port the pakcet is heading to
 - `-j` specifies what to do with the packet when it's received (e.g. REDIRECT, REJECT)
 - `-to-port` specifies what port we should forward the packet on 

 - Example route to FORWARD incoming traffic
```bash
iptables -t nat -A PREROUTING -p tcp -destination-port 80 -j REDIRECT -to-port 10000
``` 


### ARP Table

 - View ARP Table
```bash
ip n
```

 - Add a new entry
```bash
ip n add [IP_ADDRESS] lladdr [MAC] dev [INTERFACE] nud perm
```
- Example
```bash
ip n add 192.168.0.5 lladdr 00:1a:30:38:a8:00 dev eth0 nud perm
```

 - Delete an entry
```bash
ip n delete [IP_ADDRESS] dev [INTERFACE]
```
- Example
```bash
ip n delete 192.168.0.5 dev eth0
```

### ARP Cache Poisoning using Ettercap:
 - Launch the program will all network hosts as a target
```bash
ettercap -Tq ///
```

 - Target a specific host
```bash
ettercap -Tq -M arp:remote -i [INTERFACE] -S [TARGET1] [TARGET2]
```
	 - `-Tq` means text mode and quiet mode
	 - `-M` means we are using MITM mode
	 - `arp:remote` means we are poisoning a remote ARP cache
	 - `-i` means we are specifying the interface on which we are connected to the target
	 - `-S` means don't try and forge SSL certificates and present them to the victim
	 - NOTE: Look at the man/help page for how the target addresses should be formatted

 - Activate a pluggin once the program is running
 	- Press `P`
 	- Type the pluggin name and press `ENTER`
 	- E.g. `autoadd`. This pluggin automatically poisons new hosts when they join the network 