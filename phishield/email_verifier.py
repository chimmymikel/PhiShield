import re

class SimpleEmailVerifier:
    """Lightweight email validation without external dependencies"""
    
    # Common disposable/temporary email domains
    DISPOSABLE_DOMAINS = {
        'tempmail.com', 'mailinator.com', '10minutemail.com', 'throwawaymail.com',
        'yopmail.com', 'fakeinbox.com', 'trashmail.com', 'guerrillamail.com',
        'getairmail.com', 'temp-mail.org', 'disposablemail.com', 'tempail.com',
        'maildrop.cc', 'getnada.com', 'tmpmail.org', 'temp-mail.io', 'sharklasers.com',
        'guerrillamail.net', 'guerrillamail.org', 'guerrillamail.biz', 'spam4.me',
        'fake-mail.com', 'fakemail.com', 'fakemail.net', 'fakemail.org', 'fakemail.io',
        'fakemailgenerator.com', 'fakemail.net', 'fakemail.org', 'fakemail.io',
        'mailnesia.com', 'mailcatch.com', 'tempemail.net', 'tempemail.com',
        'tempinbox.com', 'tempmail.net', 'tempmail.org', 'tempmail.io',
        'mytrashmail.com', 'trashmail.net', 'trashmail.org', 'trashmail.io',
        'discard.email', 'discardmail.com', 'discardmail.de',
        'jetable.org', 'jetable.net', 'jetable.com'
    }
    
    @staticmethod
    def is_valid_email(email):
        """Basic email validation"""
        if not email:
            return False, "Email is required"
        
        email = email.lower().strip()
        
        # 1. Basic syntax check
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Invalid email format. Please use a valid email address."
        
        # 2. Check for disposable domains
        domain = email.split('@')[1].lower()
        if domain in SimpleEmailVerifier.DISPOSABLE_DOMAINS:
            return False, "Temporary or disposable email addresses are not allowed. Please use a permanent email address."
        
        return True, "Email appears valid"


def validate_email_domain(email):
    """
    Quick validation for use in Django forms
    """
    is_valid, message = SimpleEmailVerifier.is_valid_email(email)
    if not is_valid:
        from django import forms
        raise forms.ValidationError(message)
    return email