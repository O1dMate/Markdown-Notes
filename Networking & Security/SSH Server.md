# SSH Server (Debian)

### Installing SSH Server
```bash
sudo apt install openssh-server
```

### Configure Private Key Access ONLY
##### Open SSHD Config
```bash
sudo nano /etc/ssh/sshd_config
```

##### Uncomment the following Lines:
```bash
Port 22
ListenAddress 0.0.0.0

HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
HostKey /etc/ssh/ssh_host_ed25519_key

PermitRootLogin prohibit-password
StrictModes yes

PubkeyAuthentication yes

AuthorizedKeysFile		.ssh/authorized_keys

HostbasedAuthentication no
PasswordAuthentication yes
PermitEmptyPasswords no
```

##### Ensure that these options are changed
```bash
PermitRootLogin no

PubkeyAuthentication yes

HostbasedAuthentication no
PasswordAuthentication no
PermitEmptyPasswords no
```

### Restart the SSH Server
##### Restart the server
```bash
sudo systemctl restart sshd
```

##### Ensure there are no server errors
```bash
sudo systemctl status sshd
```


### Generate a Public/Private Key Pair Using one of the Following
```bash
ssh-keygen -t rsa -b 4096
ssh-keygen -t ecdsa -b 521
ssh-keygen -t ed25519
```

`-t` means the type of key.  
`-b` means the bit size of the key.  
`-f` mean specify the file name (not needed in this case as we will be prompted for it).  

**Key Types**:
 - `rsa` - Rivest Shamir Adleman, 2048 or 4096 bits are recommended.
 - `ecdsa` - Elliptic Curve Digital Signature Algorithm (better variant of DSA), supports 256, 384 and 521 bit keys.
 - `ed25519` - An EdDSA signature scheme using SHA-512 and Curve25519.



Once you run the command you will have a private key `FILE_NAME` and a public key `FILE_NAME.pub`

### Add the Public Key to Server's Authorized Keys
If the directory `~/.ssh` and file `authorized_keys` isn't already created, create it:
```bash
cd ~
mkdir .ssh
nano .ssh/authorized_keys
```

Copy the contents of the Public Key file you just created and paste it on a new line of the `authorized_keys` file.


### Restart the SSH Server
```bash
sudo systemctl restart sshd
```

### SSH into your Host on Linux
You can use `localhost` as the IP address to test the key.
```bash
ssh -i PRIVATE_KEY_FILE USER@IP
```

`-i` is the location of the private key file.  
`-p` is the port (22 is default).  



### SSH into your Host on Windows
Putty doesn't like the format that the private key comes in from ssh-keygen. You can get around this by connecting to your host using the private key with a program called `WinSCP`. When you select the private key it will prompt you asking you if you want to save it in Putty format. Click yes. You can now use this new private key file to connect to your host via Putty on Windows.