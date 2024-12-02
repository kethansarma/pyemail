import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email():
    sender = "kethansarma@example.com"
    recipient = "kethansarma@gmail.com"
    subject = "Test Email from MailHog"
    body = "This is a test email sent to MailHog using Python."

    # Create email message
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        print("Connecting to MailHog SMTP server...")
        # Connect to MailHog SMTP server (default: localhost:1025)
        with smtplib.SMTP("localhost", 1025) as server:
            server.sendmail(sender, recipient, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    send_email()
