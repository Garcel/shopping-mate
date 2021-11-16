from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_vanilla_user(self, email, password, **kwargs):
        kwargs.setdefault('is_superuser', False)
        kwargs.setdefault('is_staff', False)

        if kwargs.get('is_staff') is True:
            raise ValueError('Vanilla user must not have is_staff=True.')

        if kwargs.get('is_superuser') is True:
            raise ValueError('Vanilla user must not have is_superuser=True.')

        return self._create_user(email, password, **kwargs)

    def create_staff_user(self, email, password, **kwargs):
        kwargs.setdefault('is_superuser', False)

        if kwargs.get('is_superuser') is True:
            raise ValueError('Staff user must not have is_superuser=True.')

        extra_args = kwargs | {'is_staff': True}

        return self._create_user(email, password, **extra_args)

    def create_superuser(self, email, password, **kwargs):
        extra_args = kwargs | {'is_superuser': True, 'is_staff': True}

        return self._create_user(email, password, **extra_args)

    # helper methods
    def _create_user(self, email, password, **kwargs):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user
