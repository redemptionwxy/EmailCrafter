import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def create_eml_file(from_addr, to_addr, subject, body, attachments, output_path):
    # Create the multipart message
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject

    # Attach the body text
    msg.attach(MIMEText(body, 'plain'))

    # Attach files
    for attachment_path in attachments:
        if os.path.exists(attachment_path):
            # Open the file in binary mode
            with open(attachment_path, 'rb') as attachment_file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment_file.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={os.path.basename(attachment_path)}'
                )
                msg.attach(part)
        else:
            print(f"Warning: Attachment not found: {attachment_path}")

    # Save the message to .eml file
    with open(output_path, 'w') as eml_file:
        eml_file.write(msg.as_string())

    print(f"EML file saved to: {output_path}")

# Example usage
if __name__ == "__main__":
    from_addr = "sender@example.com"
    to_addr = "recipient@example.com"
    subject = "Test Email with Attachments"
    body = "This is a test email created locally with attachments."
    attachments = ["path/to/attachment1.pdf", "path/to/attachment2.jpg"]  # Replace with actual file paths
    output_path = "test_email.eml"  # Output file name

    create_eml_file(from_addr, to_addr, subject, body, attachments, output_path)