from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
import datetime
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes

# Generate {key, public_key}
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

# in this case subject and issuer are same
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Company"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"mysite.com"),
])

# sign the cert
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
    datetime.datetime.utcnow() + datetime.timedelta(days=10)
).add_extension(
    x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
    critical=False,
).sign(key, hashes.SHA256(), default_backend())  # in this case, CA_key = key


# Write our certificate out to disk.
with open("certificate.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

# get public_key from cert
public_key = cert.public_key()
print(public_key == cert.public_key())
if isinstance(public_key, rsa.RSAPublicKey):
    print(1)
elif isinstance(public_key, ec.EllipticCurvePublicKey):
    print(2)
else:
    pass

# get CA_pubk from disk
pem_issuer_public_key = key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
issuer_public_key = load_pem_public_key(
    pem_issuer_public_key, default_backend())

# get cert from disk
pem_data_to_check = cert.public_bytes(encoding=serialization.Encoding.PEM)
cert_to_check = x509.load_pem_x509_certificate(
    pem_data_to_check, default_backend())

# check if cert is associate with CA_public_key
issuer_public_key.verify(
    cert_to_check.signature,
    cert_to_check.tbs_certificate_bytes,
    # Depends on the algorithm used to create the certificate
    padding.PKCS1v15(),
    cert_to_check.signature_hash_algorithm,
)

# then the public_key and domain is confirmed by the CA
