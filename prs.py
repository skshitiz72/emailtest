import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

# GitHub API credentials
GITHUB_USERNAME = 'skshitiz72'
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

# Email configuration
SMTP_SERVER = 'smtp.outlook.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'shitizkumar72@outlook.com'
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
RECIPIENT_EMAIL = 'shitizkumar20@gmail.com'

# Repository information
REPO_OWNER = 'bregman-arie'
REPO_NAME = 'devops-exercises'

# Get the date range for the past week
today = datetime.now()
week_ago = today - timedelta(days=7)
date_range = f'{week_ago.date()}..{today.date()}'

# Make the API request to fetch pull requests
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}
params = {
    'state': 'all',
    'base': 'master',
    'sort': 'created',
    'direction': 'desc',
    'q': f'is:pr repo:{REPO_OWNER}/{REPO_NAME} created:{date_range}'
}
response = requests.get('https://api.github.com/search/issues', headers=headers, params=params)
response.raise_for_status()
data = response.json()

# Extract pull request details
pull_requests = {
    'Opened': [pr for pr in data['items'] if pr['state'] == 'open'],
    'Closed': [pr for pr in data['items'] if pr['state'] == 'closed'],
    'Draft': [pr for pr in data['items'] if pr['state'] == 'draft']
}

# Prepare the email content
subject = f'Pull Request Summary - {REPO_OWNER}/{REPO_NAME}'
body = '\n\n'.join([f'{status} Pull Requests ({len(prs)}):\n{[pr["title"] for pr in prs]}' for status, prs in pull_requests.items()])

# Create the email message
message = MIMEMultipart()
message['From'] = EMAIL_ADDRESS
message['To'] = RECIPIENT_EMAIL
message['Subject'] = subject
message.attach(MIMEText(body, 'plain'))

# Send the email
with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, message.as_string())

# Print the details of the email sent
print(f'From: {EMAIL_ADDRESS}')
print(f'To: {RECIPIENT_EMAIL}')
print(f'Subject: {subject}')
print('Body:')
print(body)

