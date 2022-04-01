from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'


# To automatic update the profile details
    def ready(self):
        import users.signals
