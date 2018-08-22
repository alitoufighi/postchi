from postchiapp.serializers import AccountSerializer
from postchi import settings
from simplecrypt import encrypt, decrypt


class SecurePassword:
    @staticmethod
    def encode(plaintext):
        """
        Encodes param `text` with app secret key
        Returns encoded text
        """
        cipher_text = encrypt(settings.SECRET_KEY, plaintext)
        return cipher_text

    @staticmethod
    def decode(cipher_text):
        """
        Decodes param `text` with app secret key
        Return decoded text
        """
        plaintext = decrypt(settings.SECRET_KEY, cipher_text)
        return plaintext


def jwt_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': AccountSerializer(user, context={'request': request}).data,
    }
