# Firewall-cmd

### List Default Zone & All Zones
```bash
firewall-cmd --list-all
firewall-cmd --list-all-zones
```

### List Ports
```bash
firewall-cmd --list-ports
```

### Add/Remove Ports
To open TCP port 2222:
```bash
firewall-cmd --add-port=2222/tcp
```

To close TCP port 2222:
```bash
firewall-cmd --remove-port=2222/tcp
```

### Add Port Permanent
To open TCP port 2222 that will stay in the config after the a reload:
```bash
firewall-cmd --add-port=2222/tcp --permanent
```

### Reload
```bash
firewall-cmd --reload
```

### Stop/Start Service
```bash
systemctl start firewalld.service
systemctl stop firewalld.service
```