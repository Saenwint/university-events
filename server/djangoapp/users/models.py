from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, 
    PermissionsMixin, 
    BaseUserManager,
)
from django.utils import timezone


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Создаёт и сохраняет пользователя с указанным email и паролем"""
        if not email:
            raise ValueError('Email обязателен для регистрации')
        
        email = self.normalize_email(email)
        
        user = self.model(email=email, **extra_fields)
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя"""
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='Email')
    password = models.CharField(max_length=128, verbose_name='Пароль')
    
    balance = models.IntegerField(default=0, verbose_name='Баланс ЛЭТИ-коинов')
    
    is_confirmed = models.BooleanField(default=False, verbose_name='Почта подтверждена')
    is_admin = models.BooleanField(default=False, verbose_name='Администратор')
    
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']

    def get_full_name(self):
        """Возвращает полное имя пользователя."""
        return f'{self.first_name} {self.last_name}'
    
    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'
    
    @property
    def is_staff(self):
        """Определяет, является ли пользователь сотрудником."""
        return self.is_admin
