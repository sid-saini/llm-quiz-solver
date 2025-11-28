import pandas as pd
import numpy as np
import requests
import base64
import io
from PIL import Image
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    """Handle various data processing tasks"""
    
    @staticmethod
    def download_file(url, save_path=None):
        """Download file from URL"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
            
            return response.content
        except Exception as e:
            logger.error(f"Download error: {e}")
            return None
    
    @staticmethod
    def parse_pdf(content):
        """Extract text from PDF"""
        try:
            pdf_file = io.BytesIO(content)
            reader = PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"PDF parse error: {e}")
            return None
    
    @staticmethod
    def parse_html(content):
        """Parse HTML content"""
        try:
            soup = BeautifulSoup(content, 'html.parser')
            return soup
        except Exception as e:
            logger.error(f"HTML parse error: {e}")
            return None
    
    @staticmethod
    def load_csv(content):
        """Load CSV data"""
        try:
            return pd.read_csv(io.StringIO(content.decode('utf-8')))
        except Exception as e:
            logger.error(f"CSV load error: {e}")
            return None
    
    @staticmethod
    def load_json(content):
        """Load JSON data"""
        try:
            import json
            return json.loads(content.decode('utf-8'))
        except Exception as e:
            logger.error(f"JSON load error: {e}")
            return None
    
    @staticmethod
    def image_to_base64(image_path):
        """Convert image to base64 data URI"""
        try:
            with open(image_path, 'rb') as f:
                img_data = f.read()
            b64 = base64.b64encode(img_data).decode('utf-8')
            
            # Detect image type
            img_type = 'png'
            if image_path.lower().endswith('.jpg') or image_path.lower().endswith('.jpeg'):
                img_type = 'jpeg'
            
            return f"data:image/{img_type};base64,{b64}"
        except Exception as e:
            logger.error(f"Image encoding error: {e}")
            return None
