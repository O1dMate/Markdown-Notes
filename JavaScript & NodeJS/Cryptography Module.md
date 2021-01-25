# JavaScript Crypto Module

## Symmetric Encryption (AES-256 Counter-Mode)
```javascript
const crypto = require('crypto');

let key = Buffer.from('0000111122223333444455556666777788889999aaaabbbbccccddddeeeeffff', 'hex')
let iv = Buffer.from('0123456789abcdef0123456789abcdef', 'hex')
let secret_msg = Buffer.from('To be Encrypted!', 'utf-8');

// Encrypt
let cipher = crypto.createCipheriv('aes-256-ctr', key, iv);
let encrypted = cipher.update(secret_msg);

// Decrypt
let decipher = crypto.createDecipheriv('aes-256-ctr', key, iv);
let decrypted = decipher.update(encrypted, 'hex');

console.log(`\nEncryption Key: ${key.toString('hex')}`)
console.log(`IV: \t\t${iv.toString('hex')}\n`)

console.log(`Plain-text: \t${secret_msg.toString('utf-8')}`);
console.log(`Plain-text: \t${secret_msg.toString('hex')}`);
console.log(`Encrypted: \t${encrypted.toString('hex')}`);
console.log(`Encrypted: \t${encrypted.toString('base64')}`);
console.log(`Decrypted: \t${decrypted.toString('hex')}`);
console.log(`Decrypted: \t${decrypted.toString('utf-8')}\n`);
```

<br>

## Hashing Strings
```javascript
const crypto = require('crypto');

// Get a list of supported Hash Algorithms
console.log(crypto.getHashes());

// String to be hashed
let msgToHash = 'Password1';

// Create Hash Functions
let MD4_HashFunction = crypto.createHash('md4');
let NTLM_HashFunction = crypto.createHash('md4');
let SHA256_HashFunction = crypto.createHash('sha256');
let SHA3_256_HashFunction = crypto.createHash('sha3-256');

// Add data to the hash function
MD4_HashFunction.update(msgToHash);
NTLM_HashFunction.update(Buffer.from(msgToHash, 'utf16le'));
SHA256_HashFunction.update(msgToHash);
SHA3_256_HashFunction.update(msgToHash);

// Get the result
console.log('MD4:\t\t', MD4_HashFunction.digest('hex'));
console.log('NTLM:\t\t', NTLM_HashFunction.digest('hex'));
console.log('SHA256:\t\t', SHA256_HashFunction.digest('hex'));
console.log('SHA3-256:\t', SHA3_256_HashFunction.digest('hex'));
```

<br>

## Hashing a File
```javascript
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// Target file that we what to calculate the hash of
const targetFile = path.join(__dirname, 'math1.js');

// Create Hash Function
const hash = crypto.createHash('sha256');
hash.setEncoding('hex');

// Create a read stream with the target file
const inputFileStream = fs.createReadStream(targetFile);

// Hashing is complete
inputFileStream.on('end', () => {
	hash.end();
	console.log(hash.read());
});

// Read the file contents and pipe it into the hash object
inputFileStream.pipe(hash);
```

<br>

## Elliptic Curve Diffie-Hellman
```javascript
const crypto = require('crypto');

const alice = crypto.createECDH('sect571k1');
alice.generateKeys();

const bob = crypto.createECDH('sect571k1');
bob.generateKeys();

// Alice's Data
console.log("\nAlice Public:", alice.getPublicKey().toString('base64'));
console.log("Alice Private:", alice.getPrivateKey().toString('base64'), "\n");

// Bob's Data
console.log("Bob Public:", bob.getPublicKey().toString('base64'));
console.log("Bob Private:", bob.getPrivateKey().toString('base64'), "\n");

// The Shared Secret will be the same
console.log("Shared Secret: ", alice.computeSecret(bob.getPublicKey(), null, 'base64'));
console.log("Shared Secret: ", bob.computeSecret(alice.getPublicKey(), null, 'base64'), "\n");
```