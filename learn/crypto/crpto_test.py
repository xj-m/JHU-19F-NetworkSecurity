import unittest
from Crypto_manager import *
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


class Test_key_pemfy(unittest.TestCase):
    def test_RSA_pemfy(self):
        key = Crypto_manager().generate_RSA_key()
        key_pem = Crypto_manager().pemfy_private_key(key)
        key = Crypto_manager().unpemfy_private_key(key_pem)
        key_pem_again = Crypto_manager().pemfy_private_key(key)
        self.assertEqual(key_pem, key_pem_again)

    def test_EC_pemfy(self):
        key = Crypto_manager().generate_EC_key()
        key_pem = Crypto_manager().pemfy_private_key(key)
        key = Crypto_manager().unpemfy_private_key(key_pem)
        key_pem_again = Crypto_manager().pemfy_private_key(key)
        self.assertEqual(key_pem, key_pem_again)


class Test_cert(unittest.TestCase):
    def setUp(self):
        self.issuer_key = Crypto_manager().generate_RSA_key()
        self.client_key = Crypto_manager().generate_RSA_key()
        self.server_key = Crypto_manager().generate_RSA_key()
        self.client_subject = Crypto_manager().generate_subject("test_client_subject")
        self.issuer_subject = Crypto_manager().generate_subject("test_issuer_subject")
        self.client_cert = Crypto_manager().generate_cert(self.client_subject, self.issuer_subject,
                                                          self.client_key.public_key(), self.issuer_key)

    def test_generate_cert(self):
        cert_pem = Crypto_manager().pemfy_cert(self.client_cert)
        cert = Crypto_manager().unpemfy_cert(cert_pem)
        cert_pem_again = Crypto_manager().pemfy_cert(cert)
        self.assertEqual(cert_pem, cert_pem_again)

    def test_verify_cert(self):
        try:
            Crypto_manager().verify_cert(self.issuer_key.public_key(), self.client_cert)
        except Exception as e:
            print(e)
            self.assertTrue(False)
        try:
            Crypto_manager().verify_cert(self.server_key.public_key(), self.client_cert)
        except Exception as e:
            self.skipTest("pass")
            print(e)
        self.assertTrue(False)


class Test_ECDH(unittest.TestCase):
    def setUp(self):
        self.client_key = Crypto_manager().generate_EC_key()
        self.server_key = Crypto_manager().generate_EC_key()

    def test_derive_key(self):
        server_derived_key = Crypto_manager().get_EC_derived_key(
            self.server_key, self.client_key.public_key())
        client_derived_key = Crypto_manager().get_EC_derived_key(
            self.client_key, self.server_key.public_key())
        self.assertEqual(server_derived_key, client_derived_key)

    def test_signature(self):
        data = b"test sig data"
        sig = Crypto_manager().get_EC_signature(self.client_key, data)
        try:
            Crypto_manager().verify_EC_signature(self.client_key.public_key(), sig, data)
        except Exception as e:
            print(e)
            self.assertTrue(False)
        try:
            Crypto_manager().verify_EC_signature(self.client_key.public_key(), sig, data+b"1")
        except Exception as e:
            print(e)
            self.skipTest("pass")
        self.assertTrue(False)

        # A_key
        # write into file
        # A_session_key
        # A_sig = A_session_pubk[A_key]

        # B_key
        # write into file
        # B_session_key
        # B_sig = B_session_pubk[B_key]

        # B_session_key = A_session_pubk + B_session_key
        # A_session_key = B_session_pubk + A_session_key
