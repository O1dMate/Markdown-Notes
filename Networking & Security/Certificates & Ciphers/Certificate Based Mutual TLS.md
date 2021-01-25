# Certificate Based Mutual TLS

The PKCS12 Certificates that we will be creating can be used for Certificate-Based Mutual Authentication on web servers.

<br>

## Prerequisites
 - You must have a CA that can sign the certificates we will be generating.

<br>

## Generating Certificates for Users

### Create Private Key

```bash
openssl ecparam -genkey -name secp384r1 -out old-mate.key
```


### Create Certificate Signing Request
```bash
openssl req -new -sha512 -nodes -key old-mate.key -out old-mate.csr -subj "/CN=Old Mate"
```
 - Where the `CN` is the name of the user.

### Sign the CSR using our CA

```bash
openssl x509 -req -sha512 -days 1096 -in old-mate.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out old-mate.crt
```

### Convert the new Key and Certificate to PKCS12 Format
```bash
openssl pkcs12 -export -in old-mate.crt -inkey old-mate.key -name "Old Mate's Cert" -out old-mate.p12
```

 - Where `-name` is the Friendly Name for the certificate.
 - A password passphrase must also be entered this step.