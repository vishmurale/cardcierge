from django.db.models.fields import CharField
from .cipher_tools import encrypt, decrypt

"""
source: http://www.pythondiary.com/blog/Jan.13,2020/creating-transparently-encrypted-field-django.html
"""

class EncryptedField(CharField):
    def from_db_value(self, value, expression, connection):
        """ Decrypt the data for display in Django as normal. """
        return decrypt(value)
    def get_prep_value(self, value):
        """ Encrypt the data when saving it into the database. """
        return encrypt(value)