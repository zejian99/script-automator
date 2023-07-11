import os
from datetime import datetime
import openai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from config import get_settings
OPENAI_API_KEY = get_settings().OPENAI_API_KEY
FILE_PATH = get_settings().FILE_PATH
SAVE_PATH = get_settings().SAVE_PATH
openai.api_key = OPENAI_API_KEY

def generate_summary(file):
    with open(file, 'r') as f:
        todo_list = f.read()

    prompt = f"I have accomplished the following based on my todo list:\n{todo_list}\n\n Reflection: \n "
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=400,
        n=1,
        stop=None,
        temperature=0.7
    )
    summary = response.choices[0].text.strip()

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

def process_files(directory, save_path):
    files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    if not files:
        print('No text files found in the directory.')
        return

    all_summaries = []
    for file_name in files:
        file_path = os.path.join(directory, file_name)
        summary = generate_summary(file_path)

        print(f'Summary of "{file_name}":')
        print(summary)

        all_summaries.append((file_name, summary))

    current_date = datetime.now().strftime('%Y-%m-%d')
    summary_file_name = f'all_summaries_{current_date}.txt'
    summary_file_path = os.path.join(save_path, summary_file_name)
    with open(summary_file_path, 'w') as summary_file:
        for file_name, summary in all_summaries:
            summary_file.write(f'{file_name}:\n')            
            summary_file.write(summary)
            summary_file.write('\n\n')

    send_notification("All Summaries Completed", f"All summaries for the past 2 weeks have been generated.", summary_file_path)

    # Delete the original text files after sending the email notification
    for file_name in files:
        file_path = os.path.join(directory, file_name)
        os.remove(file_path)
    

directory = FILE_PATH
save_path = SAVE_PATH
process_files(directory, save_path)
