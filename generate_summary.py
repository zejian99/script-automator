import os
import subprocess
import openai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from config import get_settings

OPENAI_API_KEY = get_settings().OPENAI_API_KEY
FILE_PATH = get_settings().FILE_PATH
openai.api_key = OPENAI_API_KEY

def generate_summary(file_path, latest_file):
    with open(file_path, 'r') as file:
        todo_list = file.read()

    prompt = f"I have accomplished the following based on my todo list:\n{todo_list}\n\nReflection:\n"
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.6
    )
    summary = response.choices[0].text.strip()

    # Delete existing text files in the directory
    directory = os.path.dirname(file_path)
    for file_name in os.listdir(directory):
        if file_name.endswith('.txt'):
            os.remove(os.path.join(directory, file_name))

    # Create a new text file with the summary
    summary_file_path = os.path.join(directory, 'summary.txt')
    print(summary_file_path)
    with open(summary_file_path, 'w') as summary_file:
        summary_file.write(summary)

    send_notification("Summary Completed", f"Summary of {latest_file} has been generated.", summary_file_path)

    return summary

def send_notification(title, message, attachment_path=None):
    # Replace these with your Gmail email address and app password
    gmail_user = get_settings().GMAIL_USER
    gmail_password = get_settings().GMAIL_PASSWORD

    # Set up the email message
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = gmail_user  # Send the email to yourself, or replace with another email address
    msg['Subject'] = title
    msg.attach(MIMEText(message, 'plain'))

    # Attach the file if a path is provided
    if attachment_path:
        with open(attachment_path, 'rb') as attachment_file:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(attachment_file.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
            msg.attach(attachment)

    # Send the email
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, [msg['To']], msg.as_string())
        server.close()
        print(f'Email sent: {title}')
    except Exception as e:
        print(f'Error sending email: {e}')

def process_files(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    if not files:
        print('No text files found in the directory.')
        return

    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory, f)))
    file_path = os.path.join(directory, latest_file)
    summary = generate_summary(file_path, latest_file)

    print(f'Summary of "{latest_file}":')
    print(summary)

directory = FILE_PATH
process_files(directory)
