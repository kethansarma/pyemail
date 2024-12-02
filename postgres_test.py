import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import psycopg2
import os
import threading

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

def setup_postgres():
    q1 = """CREATE OR REPLACE FUNCTION notify_email()
    RETURNS VOID AS $$
    BEGIN
        -- Send a notification with the email ID (or any other relevant identifier)
        PERFORM pg_notify('email_channel', 'New email ID notification');
    END;
    $$ LANGUAGE plpgsql;"""
    
    q2 = """SELECT public.notify_email();"""
    conn = psycopg2.connect(
            dbname=os.environ["DB"],
            user=os.environ["USER"],
            password=os.environ["PASSWORD"],
            host=os.environ["HOST"]
        )
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    # Execute the function to create and invoke the notification
    cur.execute(q1)
    cur.execute(q2)
    print("Postgres setup complete.")

def listen_for_emails():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=os.environ["DB"],
            user=os.environ["USER"],
            password=os.environ["PASSWORD"],
            host=os.environ["HOST"]
        )
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Listen to the email_channel
        cur.execute("LISTEN email_channel;")
        print("Listening for email notifications...")

        while True:
            conn.poll()
            while conn.notifies:
                notify = conn.notifies.pop()
                email_id = notify.payload

                # Send the email based on notification
                if email_id:
                    send_email(
                        sender_email="811cff001@smtp-brevo.com",  # Replace with your Brevo email
                        sender_password="sXtgLB59dqQN0TDa",   # Replace with your Brevo API key
                        recipient_email="kethansarma@gmail.com",
                        subject="Test Email",
                        body="This is a test email sent using SMTP service."
                    )
                    # Mark the email as sent (optional, depending on your use case)
    except Exception as e:
        print(f"Error: {e}")

def main():
    # Run the setup_postgres function and listen_for_emails function in parallel
    setup_thread = threading.Thread(target=setup_postgres)
    listen_thread = threading.Thread(target=listen_for_emails)
    listen_thread.start()
    # Start both threads
    setup_thread.start()
   

    # Optionally, wait for threads to finish if needed
    # setup_thread.join()
    listen_thread.join()

if __name__ == "__main__":
    main()
