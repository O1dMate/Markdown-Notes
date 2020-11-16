# SSL/TLS Setup on Apache2 Web-Server

### Download Programs
 - Apache2
```bash
sudo apt install apache2
```

 - OpenSSL
```bash
sudo apt install openssl
```


### Generate Self Signed Cert with OpenSSL
```bash
openssl req -x509 -newkey rsa:4096 -keyout domain.key -out domain.crt -days 1460
```

 - `rsa:4096` means it's a 4096 bit RSA key
 - `-keyout domain.key` means save the private key to a file called `domain.key`
 - `-out domain.crt` means save the certificate to a file called `domain.crt` 
 - `-days 1460` means the certificate is valid for 1460 days (4 years)


### Create a new Apache Config
1. Open the folder: `/etc/apache2/sites-available/`
2. Create a new file called `your-config-name.conf`
3. Inside this file, paste this template:
```bash
<IfModule mod_ssl.c>

	# Load the headers module
	LoadModule headers_module modules/mod_headers.so

	<VirtualHost THE_SERVER_IP:443>
		# Enable HTST
		Header always set Strict-Transport-Security "max-age=63072000; includeSubdomains;"

		# Stop Click Jacking
		Header append X-FRAME-OPTIONS "DENY"

		ServerAdmin webmaster@localhost
		ServerName THE_SERVER_IP:443

		DocumentRoot /var/www/html/public

		# Enable SSL/TLS
		SSLEngine on

		# Force TLSv1.2 as only accept protocol
		SSLProtocol TLSv1.2

		# Paths to SSL/TLS Certs & Key
		SSLCertificateFile /etc/apache2/tls/domain.crt
		SSLCertificateKeyFile /etc/apache2/tls/domain.key
		SSLCertificateChainFile /etc/apache2/tls/domain.crt

		<Directory "/var/www/html/public">
	            Options FollowSymLinks
	            AllowOverride All
	            ReWriteEngine On
		</Directory>

		ErrorLog ${APACHE_LOG_DIR}/error.log
		CustomLog ${APACHE_LOG_DIR}/access.log combined

	</VirtualHost>	
</IfModule>

```

 - `<VirtualHost THE_SERVER_IP:443>` means host the server on this `THE_SERVER_IP` on port `443`. To access the server go to the URL `https://THE_SERVER_IP:443`.
 -  `DocumentRoot /var/www/html` means serve from this directory. If we put a `index.hmtl` file in this directory, it will be served when a client navigates to `https://THE_SERVER_IP:443`.
 - The path after `SSLCertificateFile` and `SSLCertificateKeyFile` are the paths to our cert and private key that we generated.
 - `SSLProtocol TLSv1.2` means only allow `TLSv1.2` for the connection.
 - If we want to support some older versions of `TLS` but we don't want to support old `SSL` versions, we can add `SSLProtocol all -SSLv2 -SSLv3` below `SSLEngine on`. This line means allow all protocols except `SSLv2` and `SSLv3`.


### Enable the Config & SSL/TLS

Open up a terminal and do the following:

 - Enable Log Rewriting
```bash
a2enmod rewrite
```

 - Enable SSL Module
```bash
a2enmod ssl
```

 - Enable Header Module
```bash
a2enmod headers
```

 - Stop Directory Browsing
```bash
a2dismod -f autoindex
```

 - Disable all configs in the `/etc/apache2/sites-available` folder
```bash
a2dissite 000-deafult.conf
a2dissite default-ssl.conf
```

 - Enable your new config
```bash
a2ensite new-config-name.conf
```

 - Restart Apache2 service
```bash
systemctl restart apache2
```
 - **Note**: you will need to enter your passphrase for your SSL/TLS cert whenever you restart the service.