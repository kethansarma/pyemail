import subprocess
import time

def send_email_thunderbird(recipient, subject, body):
    # Construct the Thunderbird command with parameters
    command = [
        'thunderbird',
        '--compose',
        f'to={recipient},subject={subject},body={body}'
    ]
    
    try:
        # Run Thunderbird command to compose email
        subprocess.run(command, check=True)
        print("Email composing in Thunderbird...")
        
        # Wait for the user to manually send the email or set up auto-send (if configured)
        time.sleep(5)  # Wait for a few seconds to give time for Thunderbird to open
        print("You can now send the email in Thunderbird.")
    
    except subprocess.CalledProcessError as e:
        print(f"Error while launching Thunderbird: {e}")

if __name__ == "__main__":
    recipient = "kethansarma@gmail.com"  # Replace with recipient's email
    subject = "Test Email"  # Email subject
    body = "This is a test email sent via Thunderbird using Python."  # Email body
    
    send_email_thunderbird(recipient, subject, body)
