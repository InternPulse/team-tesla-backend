from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):

        return (str(user.pk), str(timestamp), str(user.is_active))
    
confirm_token_generator = TokenGenerator()
