from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class SuspiciousLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    url = models.URLField(max_length=500)
    is_suspicious = models.BooleanField(default=False)
    risk_level = models.CharField(max_length=20, default='safe')
    flags = models.TextField(blank=True, null=True)
    date_checked = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_checked']
        verbose_name = 'Suspicious Link'
        verbose_name_plural = 'Suspicious Links'

    def __str__(self):
        return f"{self.url[:50]} - {self.risk_level}"


class SuspiciousMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    is_suspicious = models.BooleanField(default=False)
    risk_level = models.CharField(max_length=20, default='safe')
    flags = models.TextField(blank=True, null=True)
    date_checked = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_checked']
        verbose_name = 'Suspicious Message'
        verbose_name_plural = 'Suspicious Messages'

    def __str__(self):
        return f"Message on {self.date_checked.strftime('%Y-%m-%d %H:%M')}"


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('manager', 'Manager'),
        ('admin', 'Administrator'),
        ('security_analyst', 'Security Analyst'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Profile Information
    bio = models.TextField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    
    # Statistics
    total_checks = models.IntegerField(default=0)
    threats_detected = models.IntegerField(default=0)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    
    # Verification
    email_verified = models.BooleanField(default=True)
    
    # Profile Image
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Preferences & Settings
    receive_email_notifications = models.BooleanField(default=True)
    receive_security_alerts = models.BooleanField(default=True)
    dark_mode_enabled = models.BooleanField(default=False)
    auto_scan_links = models.BooleanField(default=False)
    show_tips = models.BooleanField(default=True)
    language = models.CharField(max_length=10, default='en', choices=[('en', 'English'), ('es', 'Spanish')])

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def success_rate(self):
        """Calculate success rate for threat detection"""
        if self.total_checks == 0:
            return 0
        return round((self.threats_detected / self.total_checks) * 100, 2)
    
    @property
    def safe_checks(self):
        """Calculate number of safe checks"""
        return self.total_checks - self.threats_detected
    
    @property
    def account_age_days(self):
        """Calculate account age in days"""
        return (timezone.now() - self.date_joined).days

    def save(self, *args, **kwargs):
        """Ensure profile stays verified"""
        self.email_verified = True
        super().save(*args, **kwargs)


# Automatic profile creation when user is created
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create user profile when a new user is created"""
    if created:
        profile = UserProfile.objects.create(user=instance)
        profile.email_verified = True
        profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Automatically save user profile when user is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()