from mage_ai.data_preparation.shared.secrets import get_secret_value
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, os

@data_exporter
def export_data(html_name, subject, list_emails):
    html_name = 'winners_notification.html'
    subject = 'Test'
    list_emails = ['vmdcortes@gmail.com']
    # Read HTML content from file
    project_path = os.environ.get('USER_CODE_PATH')
    html_path = os.path.join(project_path, 'emails', html_name)

    with open(html_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Call function to send email
    for email in list_emails:
        send_email(email, subject, html_content)

    def send_email(receiver_email, subject_email, html_content):
        # Email configurations
        sender_alias = 'contacto@andes-hosting.com'
        sender_email = get_secret_value('email_user')
        sender_password = get_secret_value('email_password')

        # Create message container - the correct MIME type is multipart/alternative
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject_email
        msg['From'] = f'Andes Hosting <{sender_alias}>'
        msg['To'] = receiver_email

        # Attach HTML content to the email
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)

        # Send the email
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_alias, receiver_email, msg.as_string())
            print(f"Email sent to {receiver_email} successfully!")
        except Exception as e:
            print(f"Failed to send email to {receiver_email}:", str(e))
        finally:
            server.quit()
