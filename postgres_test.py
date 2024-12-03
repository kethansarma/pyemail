import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import psycopg2
import os


def send_email(sender_email, sender_password, recipient_email, subject, body):
    """
    Send an email using Brevo's SMTP server.
    """
    smtp_server = "smtp-relay.brevo.com"
    port = 587  # Use 465 for SSL or 587 for TLS

    try:
        # Create the email
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Connect to Brevo's SMTP server and send the email
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
            print(f"Email sent successfully to {recipient_email}!")
    except Exception as e:
        print(f"Failed to send email: {e}")


def query_and_email():
    """."""
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=os.environ["DB"],
            user=os.environ["USER"],
            password=os.environ["PASSWORD"],
            host=os.environ["HOST"],
        )
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Listen to the email_channel
        cur.execute("select count(*) from table_name;")
        result = cur.fetchall()[0][0]

        send_email(
            sender_email="811cff001@smtp-brevo.com",  # Replace with your Brevo email
            sender_password="password",  # Replace with your Brevo API key
            recipient_email="example@gmail.com",
            subject="Count Email",
            body=f"count of rows {result} in table_name",
        )
        # Mark the email as sent (optional, depending on your use case)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    query_and_email()
