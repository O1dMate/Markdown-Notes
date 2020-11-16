# Generating Certs

<br>

## 1. Create a Certificate Authority (CA)

### List OpenSSL Supported Elliptic Curves
```bash
openssl ecparam -list_curves
```


### Generate CA Private Key

```bash
openssl ecparam -genkey -name secp384r1 -out ca.key
```

 - `Note:` not all Elliptic Curves are supported by browsers. Make sure you Google whether a curve is supported before using it for a certificate.


### Generate CA Certificate

Create a config file `ca.conf` for the request like the following:

```text
basicConstraints = CA:TRUE
keyUsage = cRLSign, keyCertSign
[req]
distinguished_name = req_distinguished_name
prompt = no
[req_distinguished_name]
C   = AU
ST  = Victoria
L   = Melbourne
CN  = OldMate Root CA
```

 - The `CN` field is the value that will be shown in the `Issued To` & `Issued By` fields when viewing the cert.

Generate a Certificate for our new Certificate Authority using the Private key just generated:

```bash
openssl req -x509 -new -sha512 -nodes -key ca.key -days 7307 -out ca.crt -config ca.conf
```

 - `-x509` outputs a self signed certificate instead of a Certificate Signing Request (CSR).
 - `-nodes` means don't encrypt the private key.
 - `-key ` is the Private Key we are signing this with.

<br>
<br>


## 2. Create and Sign Host Certificates

 - These certificates can be used for web servers and will be signed by our new CA.
 - The CA we created should be added in our browser as a Trusted Root CA.

### Generate Private Key for the Hosts
```bash
openssl ecparam -genkey -name secp384r1 -out host1.key
```


### Generate Certificate Signing Request (CSR) for the new Certificate

Create a config file `host1.conf` for the request like the following:
```text
[req]
default_md	= sha512
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
[req]
distinguished_name = req_distinguished_name
req_extensions = req_ext
prompt = no
[req_distinguished_name]
C   = AU
ST  = Victoria
L   = Melbourne
O   = OldMateTech
OU  = R&D
CN  = host1.oldmate
[req_ext]
subjectAltName = @alt_names
[alt_names]
DNS.1 = host1.oldmate
DNS.2 = host2.oldmate
```

Create a certificate using the private that we just generated. This certificate will then need to be signed by our CA. This is why it's called a Signing Request.

```bash
openssl req -new -sha512 -nodes -key host1.key -out host1.csr -config host1.conf
```

 - Notice that we don't use the `-x509` flag this time as we are creating a CSR, not an actual certificate.


### Verify the CSR is Correct

The details of the Certificate Signing Request will be printed out.

```bash
openssl req -noout -text -in host1.csr
```


### Sign the CSR using our CA

 - The certificate will still be useable if it's not a SAN Cert, however, we will not have a green padlock in the browser. Even if the CA is imported as a Trusted Root Cert, it will still not be green unless it's a valid SAN Cert.

 Create a config file `host1-ext.conf` for the certificate with additional parameters that are required to make it a valid Subject Alternative Name (SAN) Certificate:

```text
basicConstraints = CA:FALSE
nsCertType = server
nsComment = "Web App Testing Cert"
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer:always
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names
[alt_names]
DNS.1 = host1.oldmate
DNS.2 = host2.oldmate
```

Sign the certificate using our new CA:

```bash
openssl x509 -req -sha512 -days 45 -in host1.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out host1.crt -extfile host1-ext.conf
```

 - Notice that we use the `x509` not `-x509` and `-req` not `req`. OpenSSL syntax isn't amazing.


### Verify the Certificate is Correct

The details of the certificate will be printed out.

```bash
openssl x509 -noout -text -in host1.crt
```



<br>


## Notes

### Good Video Resource
 - [https://www.youtube.com/watch?v=LIlyb_rRnPY](https://www.youtube.com/watch?v=LIlyb_rRnPY)

### GitHub From the Video
 - [https://github.com/StormWindStudios/OpenSSL-Notes](https://github.com/StormWindStudios/OpenSSL-Notes)