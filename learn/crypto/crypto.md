# python crypto


## Basic

[!!非对称加密理解](https://www.cnblogs.com/JeffreySun/archive/2010/06/24/1627247.html)

**signature**: a msg with a encrypted hash, hash is to prove the msg is true

**certificate**: contains a public key, and the domain name this public key associate with

**trust**: associate a public key with the domain

## CRFC

```sequence
Note right of A: {CA_key, CA_pubk}
Note right of A: {A_key, A_pubk}
Note right of A: certA = (A_addr, A_pubk)[CA_key]
Note right of A: {A_session_key, A_session_pubk}
Note right of A: A_sig = A_session_pubk[A_key]
A-B:{ NOT_STARTED, ?A_pubk, sigA, certA}
Note left of B: CA.verify(A_cert.addr, A_addr)
Note left of B: A_session_pubk = A_sig[A_cert.A_pubk]
Note left of B: {B_session_key, B_session_pubk}
Note left of B: session_key = A_session_pubk + B_session_key
Note left of B: {B_key, B_pubk}
Note left of B: certB = (B_addrB, B_pubk)[CA_key]
Note left of B: B_sig = pubkB[B_key]
B-A:{ SUCCESS, B_pubk, B_sig, B_cert}
Note right of A: CA.verify(B_cert, B_addr)
Note right of A: B_session_pubk = B_sig[B_cert.A_pubk]
Note right of A: session_key = B_session_pubk+A_session_key
```

### inline

A: {`signkA`, `verikA`}, `certA` = (`addrA`, `verikA`)[`signkA`]

A: {`keyA`, `pubkA`}

A: `sigA` = `pubkA`[`signkA`]

=> HandshakePacket{status: NOT_STARTED, pk: `pubkA`, signature: `sigA`, cert: `certA`}

B: issuer.verify(`certA`, `addrA`)

B: {`keyB`, `pubkB`}

B: `verikA`.verify(`sigA`)

B: `shared_secret` = `pubkA`+`keyB`

B: {`signkB`, `verikB`}, `certB` = (`addrB`, `verikB`)[`signkB`]

B: `sigB` = `pubkB`[`signkB`]

<= HandshakePacket{status:SUCCESS, pk: `pubkB`, cert: `certB`, signature: `sigB`}

A: issuer.verify(`certB`, `addrB`)

A: `verikB`.verify(`sigB`)

A: `shared_secret` = `pubkB`+`keyA`

=> HandshakePacket{status:SUCCESS}

## certificate

### Certificate Signing Request (CSR)

```sequence
Note left of A: generate {key, public_key}
A-CA: CSR[key]
Note right of CA: verify signature
CA-A: Certificate{pubkA, domain}[CA]
```

load key:`load_pem_private_key()`

### self signed certificate

> usually only for local test, where nobody need to trust this

#### sign a cert

1. use RSA generate {key, public_key}
2. save key
3. sign cert with key
4. save cert

```python
import datetime
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
# Generate {privkA, pubkA}
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
# Write our key to disk for safe keeping
with open("key.pem", "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(
            b"passphrase"),
    ))
# Various details about who we are. For a self-signed certificate the
# subject and issuer are always the same.
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Company"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"mysite.com"),
])
cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.utcnow()
).not_valid_after(
    # Our certificate will be valid for 10 days
    datetime.datetime.utcnow() + datetime.timedelta(days=10)
).add_extension(
    x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
    critical=False,
    # Sign our certificate with our private key
).sign(key, hashes.SHA256(), default_backend())
# Write our certificate out to disk.
with open("certificate.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

```

#### get public_key from a cert

```Python
public_key = cert.public_key()
if isinstance(public_key, rsa.RSAPublicKey):
    # Do something RSA specific
elif isinstance(public_key, ec.EllipticCurvePublicKey):
    # Do something EC specific
else:
    # Remember to handle this case
```

#### verify a certificate

```Python
# prepare pubkA and certA
pem_issuer_public_key = key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
pem_data_to_check = cert.public_bytes(encoding=serialization.Encoding.PEM)
issuer_public_key = load_pem_public_key(
    pem_issuer_public_key, default_backend())
cert_to_check = x509.load_pem_x509_certificate(
    pem_data_to_check, default_backend())
# check if certA is associate with pubkA
issuer_public_key.verify(
    cert_to_check.signature,
    cert_to_check.tbs_certificate_bytes,
    padding.PKCS1v15(),
    cert_to_check.signature_hash_algorithm,
)
```
