from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from phishield.models import UserProfile

class Command(BaseCommand):
    help = 'Fix application issues - verify users and check system'
    
    def handle(self, *args, **options):
        self.stdout.write("🔧 Fixing PhiShield Application...")
        
        # Fix 1: Verify all existing users
        users = User.objects.all()
        verified_count = 0
        
        for user in users:
            profile, created = UserProfile.objects.get_or_create(user=user)
            if not profile.email_verified:
                profile.email_verified = True
                profile.email_verification_token = None
                profile.save()
                verified_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Verified: {user.username}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'🎉 Verified {verified_count} users!')
        )
        
        # Fix 2: Show system status
        self.stdout.write("\n📊 System Status:")
        self.stdout.write(f"   Total Users: {User.objects.count()}")
        self.stdout.write(f"   Total Profiles: {UserProfile.objects.count()}")
        
        self.stdout.write(
            self.style.SUCCESS('\n🚀 Application is ready!')
        )