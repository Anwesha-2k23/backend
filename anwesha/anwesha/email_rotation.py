"""
Email account rotation for load distribution and throttling avoidance.
"""
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email accounts pool (order will be rotated)
EMAIL_ACCOUNTS = [
    {"email": "anweshatroubleshoot@gmail.com", "password": "asly xjma ceez yfgt"},
    {"email": "dev.anweshaiitp@gmail.com", "password": "iptl pffk jusy kjxd"},
    {"email": "authanwesha@gmail.com", "password": "mpmo ezvg smze xtdc"},
    {"email": "authiitp@gmail.com", "password": "rozz exui vkks edju"},
    {"email": "anwesha.auth@gmail.com", "password": "oply cpvw asug nkce"},
]

# Thread-safe counter for rotation
_rotation_lock = threading.Lock()
_current_index = 0


def get_next_email_account():
    """Get next email account in rotation (round-robin)"""
    global _current_index
    with _rotation_lock:
        account = EMAIL_ACCOUNTS[_current_index]
        _current_index = (_current_index + 1) % len(EMAIL_ACCOUNTS)
        return account


def send_email_rotated(to_email, subject, body, html=False):
    """
    Send email using rotated account. Falls back to next account if one fails.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Email body (plain text or HTML)
        html: Whether body is HTML (default False)
    
    Returns:
        True if sent successfully, False otherwise
    """
    attempts = len(EMAIL_ACCOUNTS)
    
    for attempt in range(attempts):
        account = get_next_email_account()
        
        try:
            msg = MIMEMultipart('alternative') if html else MIMEText(body)
            msg['From'] = account['email']
            msg['To'] = to_email
            msg['Subject'] = subject
            
            if html:
                msg.attach(MIMEText(body, 'html'))
            
            # Connect to Gmail SMTP
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(account['email'], account['password'])
                server.send_message(msg)
            
            print(f"✓ Email sent via {account['email']}")
            return True
            
        except Exception as e:
            print(f"✗ Failed to send via {account['email']}: {str(e)}")
            if attempt < attempts - 1:
                print(f"  Trying next account...")
                continue
            else:
                print(f"  All accounts failed")
                return False
    
    return False


class EmailThreadRotated(threading.Thread):
    """Thread for sending email with rotation in background"""
    def __init__(self, to_email, subject, body, html=False):
        self.to_email = to_email
        self.subject = subject
        self.body = body
        self.html = html
        threading.Thread.__init__(self)
    
    def run(self):
        send_email_rotated(self.to_email, self.subject, self.body, self.html)
