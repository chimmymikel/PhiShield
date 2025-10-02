import re
import urllib.parse

SUSPICIOUS_KEYWORDS = [
    'login', 'verify', 'secure', 'account', 'update', 'bank', 
    'confirm', 'password', 'signin', 'suspended', 'locked',
    'urgent', 'immediate', 'action', 'click', 'prize', 'winner'
]

IP_RE = re.compile(r'^\d+\.\d+\.\d+\.\d+$')


def analyze_url(url):
    """Analyze URL for phishing indicators"""
    try:
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.lower()
        flagged = []

        domain_only = domain.split(':')[0]

        if IP_RE.match(domain_only):
            flagged.append('Domain is an IP address (suspicious)')

        found = [k for k in SUSPICIOUS_KEYWORDS if k in url.lower()]
        for k in found:
            flagged.append(f'Contains suspicious keyword: "{k}"')

        if domain_only.count('-') > 2:
            flagged.append('Domain has many hyphens (potential spoofing)')

        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz']
        for tld in suspicious_tlds:
            if domain_only.endswith(tld):
                flagged.append(f'Suspicious top-level domain: {tld}')

        if '@' in url:
            flagged.append('Contains @ symbol (URL obfuscation technique)')

        if len(url) > 200:
            flagged.append('Extremely long URL (potential obfuscation)')

        if not flagged:
            result = 'safe'
        elif any(kw in url.lower() for kw in ['password', 'login', 'bank', 'signin']) or IP_RE.match(domain_only):
            result = 'dangerous'
        else:
            result = 'suspicious'

        return result, ' | '.join(flagged) if flagged else 'No threats detected'

    except Exception as e:
        return 'error', f'Error analyzing URL: {str(e)}'


def analyze_message(text):
    """Analyze text message for phishing indicators"""
    try:
        flagged = []
        
        found = [k for k in SUSPICIOUS_KEYWORDS if k in text.lower()]
        if found:
            flagged.append(f'Suspicious words: {", ".join(found[:3])}')

        urls = re.findall(r'https?://\S+', text)
        if len(urls) >= 2:
            flagged.append(f'Contains {len(urls)} links (suspicious)')
        elif len(urls) == 1:
            flagged.append('Contains a link')

        urgent_phrases = ['act now', 'urgent', 'verify your account', 'click here', 
                         'immediate action', 'suspended', 'expire', 'limited time']
        found_urgent = [p for p in urgent_phrases if p in text.lower()]
        if found_urgent:
            flagged.append(f'Urgent language detected: {", ".join(found_urgent[:2])}')

        personal_info = ['social security', 'ssn', 'credit card', 'cvv', 
                        'pin', 'date of birth', 'mother\'s maiden']
        found_personal = [p for p in personal_info if p in text.lower()]
        if found_personal:
            flagged.append('Requests personal information (HIGH RISK)')

        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        if caps_ratio > 0.3 and len(text) > 20:
            flagged.append('Excessive capitalization detected')

        if not flagged:
            result = 'safe'
        elif found_personal or len(urls) > 1 or any(kw in text.lower() for kw in ['password', 'bank account', 'ssn']):
            result = 'dangerous'
        elif flagged:
            result = 'suspicious'
        else:
            result = 'safe'

        return result, ' | '.join(flagged) if flagged else 'No threats detected'

    except Exception as e:
        return 'error', f'Error analyzing message: {str(e)}'