#emails/utils/file_parser.py

import csv
import io
import pandas as pd

def parse_uploaded_file(file):
    recipients = []

    if file.name.endswith('.csv'):
        decoded = file.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(decoded))
    elif file.name.endswith('.xlsx'):
        df = pd.read_excel(file)
        reader = df.to_dict(orient='records')
    else:
        raise ValueError("Only .csv and .xlsx files are supported")

    for row in reader:
        email = row.get('email') or row.get('Email')
        first_name = row.get('first_name') or row.get('First Name') or ''
        last_name = row.get('last_name') or row.get('Last Name') or ''
        full_name = f"{first_name} {last_name}".strip()

        if email:
            recipients.append({
                'email': email.strip(),
                'full_name': full_name,
                'first_name': first_name.strip(),
                'last_name': last_name.strip()
            })

    return recipients
