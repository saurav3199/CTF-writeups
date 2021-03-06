The challenge name was Mike's Marvelous Mystery Curves

# Description:

Mike, the System Administrator, thought it would be a good idea to implement his own Elliptic Curve Diffie Hellman key exchange using unnamed curves to use across the network. We managed to capture network traffic of the key exchange along with an encrypted file transfer. See if you can read the contents of that file.

__Note__ : The password to the AES192-CBC encrypted file is the shared key x and y coordinates from the key exchange concatenated together. (e.g. sharedKey = (12345,67890) password = “1234567890”)


# Solution:

> With the help of my teammate Lucas

From the [pcap](https://github.com/saurav3199/CTF-writeups/blob/master/TAMUctf19/assets/key_exchange.pcap) file given we obtain prime p,a and b   
```
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            a8:49:ac:8c:84:0f:84:ce
    Signature Algorithm: ecdsa-with-SHA256
        Issuer: C = US, ST = Texas, L = College Station, O = Texas A&M University, OU = tamuCTF, CN = Bob, emailAddress = bob@tamuctf.edu
        Validity
            Not Before: Oct  9 13:15:35 2018 GMT
            Not After : Nov  8 13:15:35 2018 GMT
        Subject: C = US, ST = Texas, L = College Station, O = Texas A&M University, OU = tamuCTF, CN = Bob, emailAddress = bob@tamuctf.edu
        Subject Public Key Info:
            Public Key Algorithm: id-ecPublicKey
                Public-Key:
                    196393473219
                    35161195210
                ASN1 OID: badPrime96v4
                CURVE: JustNo
                    Field Type: prime-field
                    Prime:
                        412220184797
                    A:
                        10717230661382162362098424417014722231813
                    B:
                        22043581253918959176184702399480186312
                    Generator:
                        56797798272
                        349018778637
        X509v3 extensions:
            X509v3 Subject Key Identifier: 
                84:25:43:45:2C:0C:7E:1C:85:BC:E9:AF:44:BE:42:A1:84:D6:D2:27
            X509v3 Authority Key Identifier: 
                keyid:84:25:43:45:2C:0C:7E:1C:85:BC:E9:AF:44:BE:42:A1:84:D6:D2:27

            X509v3 Basic Constraints: critical
                CA:TRUE
    Signature Algorithm: ecdsa-with-SHA256
         30:46:02:21:00:d4:45:84:18:e3:06:8d:bb:3b:e9:4d:68:a9:
         56:f4:af:e0:28:23:26:7d:4d:1e:84:2b:e8:c4:d3:ac:85:a9:
         c8:02:21:00:e9:ef:bc:0d:fa:3a:85:c4:39:1a:16:3b:6a:c0:
         6a:3f:ac:f2:7a:5f:49:ea:86:e4:18:5e:ac:91:75:31:b3:5b
```

and use it in the [script](https://github.com/saurav3199/CTF-writeups/blob/master/TAMUctf19/ecc.py)
So we got the flag by decrypting [encrypted file](https://github.com/saurav3199/CTF-writeups/blob/master/TAMUctf19/assets/enc) using aes key from the script.

The decrypted file is then [aes-dec.txt](https://github.com/saurav3199/CTF-writeups/blob/master/TAMUctf19/assets/odt-IV-e239af1f105fd13c8d0ff25dbb8a33f2.dat)


