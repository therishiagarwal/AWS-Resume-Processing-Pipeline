import json
import boto3
import re
from io import BytesIO
from datetime import datetime
import PyPDF2

# Initialize AWS clients
s3_client = boto3.client('s3')
dynamodb = boto3.client('dynamodb')

# DynamoDB table name
TABLE_NAME = "ResumesTable"

def lambda_handler(event, context):
    # Get the S3 bucket and object key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    # Download the PDF file from S3
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    pdf_file = BytesIO(response['Body'].read())
    
    # Extract text from PDF
    text = extract_text_from_pdf(pdf_file)
    
    # Extract fields
    extracted_data = extract_fields(text)
    
    # Save to DynamoDB
    resume_id = object_key.split('/')[-1]  # filename as ID
    save_to_dynamodb(resume_id, extracted_data)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Successfully processed the resume and stored extracted data into DynamoDB!')
    }

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF."""
    text = ''
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:
        text += page.extract_text() or ''
    return text

def extract_fields(text):
    """Extract name, email, phone, skills, etc."""
    email = extract_email(text)
    phone = extract_phone(text)
    linkedin = extract_linkedin(text)
    name = extract_name(text)
    skills = extract_skills(text)
    
    return {
        'Name': name or "Not Found",
        'Email': email or "Not Found",
        'Phone': phone or "Not Found",
        'LinkedIn': linkedin or "Not Found",
        'Skills': skills or [],
        'Timestamp': datetime.utcnow().isoformat() + "Z"
    }

def extract_email(text):
    match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return match.group() if match else None

def extract_phone(text):
    match = re.search(r'\b(\+?\d{1,3})?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', text)
    return match.group() if match else None

def extract_linkedin(text):
    match = re.search(r'https?://(www\.)?linkedin\.com/in/[A-Za-z0-9\-_/]+', text)
    return match.group() if match else None

def extract_name(text):
    # Very basic: Assume the first line contains the name
    lines = text.split('\n')
    for line in lines:
        if line.strip():
            return line.strip()
    return None

def extract_skills(text):
    # Look for some common keywords
    keywords = ['Python', 'AWS', 'Django', 'Flask', 'Java', 'Node.js', 'React', 'Machine Learning', 'Deep Learning', 'Lambda', 'SQL']
    found_skills = [skill for skill in keywords if skill.lower() in text.lower()]
    return found_skills

def save_to_dynamodb(resume_id, data):
    """Save parsed data to DynamoDB."""
    try:
        item = {
            'ResumeID': {'S': resume_id},
            'Name': {'S': data['Name']},
            'Email': {'S': data['Email']},
            'Phone': {'S': data['Phone']},
            'LinkedIn': {'S': data['LinkedIn']},
            'Skills': {'SS': data['Skills']},
            'Timestamp': {'S': data['Timestamp']}
        }
        dynamodb.put_item(TableName=TABLE_NAME, Item=item)
        print(f"Saved resume {resume_id} successfully!")
    except Exception as e:
        print(f"Error saving to DynamoDB: {e}")
