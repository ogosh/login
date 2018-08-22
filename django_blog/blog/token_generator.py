from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class GenerateMyEmailToken(PasswordResetTokenGenerator):
    def make_hash_value(self, user, timestamp):
        hashed_token = (six.text_type(user.pk) + six.text_type(timestamp) +
                      six.text_type(user.is_active))
        return hashed_token

email_activation_token = GenerateMyEmailToken()
