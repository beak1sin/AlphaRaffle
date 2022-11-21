from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, rs, timestamp):
        return (text_type(rs.member_id)) + text_type(timestamp)


account_activation_token = AccountActivationTokenGenerator()