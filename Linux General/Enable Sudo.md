# How to Enable Sudo

### Become root
```bash
su
```

### Install Sudo
```bash
apt install sudo
```

### Add Desired User to Sudoers File
```bash
nano /etc/sudoers
```
 - Find the line `root ALL=(ALL:ALL) ALL`
 - Underneath add the line `USERNAME  ALL=(ALL:ALL) ALL`
 - This will allow the user to run **EVERYTHING as root!!!**
    - This is **DANGEROUS**, please make sure you know what this means!!!