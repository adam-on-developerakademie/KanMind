from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    """
    Custom User Model mit zusätzlichen Feldern
    """
    fullname = models.CharField(max_length=150, verbose_name="Vollständiger Name")
    email = models.EmailField(unique=True, verbose_name="E-Mail-Adresse")
    
    # Username nicht verwenden, stattdessen E-Mail
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fullname']
    
    class Meta:
        verbose_name = "Benutzer"
        verbose_name_plural = "Benutzer"
        ordering = ['email']
    
    def __str__(self):
        return f"{self.fullname} ({self.email})"