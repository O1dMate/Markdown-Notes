# Setting up Apache2 Web Server on Debian

## Installing & Testing
 - Install apache2
```bash
sudo apt install apache2
```

 - Enable PHP module on the server
```bash
sudo a2enmod php7.2
```

 - Retrieve the page that is being served when you navigate to the server URL:
```bash
curl localhost
```

## Status
 - Check the status of the apache2 service
```bash
systemctl status apache2
```

 - Restart the apache2 service
```bash
systemctl restart apache2
```


## What is being served
Open the file: `/etc/apache2/sites-available/000-default.conf`

 - The line `<VirtualHost *:80>` means serve any IP on port `80`.
 - Further down you will see a `Document Root /var/www/html`, this means serve from the directory `/var/www/html/`.



## Logs & History

 - Check the log history of the apache2 service
```bash
journalctl -u apache2.service
```

 - Print out error log that will track live errors
```bash
sudo tail -f /var/log/apache2/error.log
```