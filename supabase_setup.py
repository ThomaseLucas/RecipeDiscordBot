from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_API_KEY')

supabase: Client = create_client(url, key)