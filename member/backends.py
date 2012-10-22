from member.models import Member


class ModelBackend(object):
    """
    Authenticates against django.contrib.auth.models.User.
    """
    supports_inactive_user = True

    # TODO: Model, login attribute name and password attribute name should be
    # configurable.
    def authenticate(self, username=None, password=None):
        try:
            user = Member.objects.get(username=username)
            if user.check_password(password):
                return user
        except Member.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Member.objects.get(pk=user_id)
        except Member.DoesNotExist:
            return None