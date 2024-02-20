# dump_data_script.py
import os
import django
from django.core.management import call_command

# Setting up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UK_Estate_Agent_Official.settings')
django.setup()

# File to store the dumped data
output_file = 'data.json'

# Open the file with UTF-8 encoding and dump data
with open(output_file, 'w', encoding='utf-8') as f:
    call_command('dumpdata', '--exclude', 'auth.permission', '--exclude', 'contenttypes', stdout=f)
