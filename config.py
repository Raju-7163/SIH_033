import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Export configurations
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/farmlinkai')
DATA_GOV_API_KEY = os.getenv('DATA_GOV_API_KEY', 'your-api-key-here')
SECRET_KEY = os.getenv('SECRET_KEY', 'change-this-to-a-random-secret')
UPLOAD_FOLDER = 'static/uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB limit
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
