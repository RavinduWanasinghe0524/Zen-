"""
Zen Voice Assistant - AI Vision Module
Multi-modal AI capabilities: screen analysis, image understanding, OCR, generation.
"""

import logging
from typing import Optional, List
import base64
from io import BytesIO
from config import Config

logger = logging.getLogger(__name__)


class AIVision:
    """Multi-modal AI vision capabilities."""
    
    def __init__(self, provider="openai"):
        """
        Initialize AI vision system.
        
        Args:
            provider: Vision provider (openai, gemini)
        """
        self.provider = provider
        self.client = None
        self._initialize_provider()
    
    def _initialize_provider(self):
        """Initialize the vision provider."""
        try:
            if self.provider == "openai":
                from openai import OpenAI
                self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
                logger.info("OpenAI Vision initialized")
            elif self.provider == "gemini":
                import google.generativeai as genai
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.client = genai.GenerativeModel('gemini-1.5-pro-vision')
                logger.info("Gemini Vision initialized")
        except Exception as e:
            logger.error(f"Failed to initialize vision provider: {e}")
            raise
    
    def capture_screen(self, region: Optional[tuple] = None) -> bytes:
        """
        Capture screenshot.
        
        Args:
            region: Optional (x, y, width, height) region to capture
            
        Returns:
            Screenshot as bytes
        """
        try:
            from PIL import ImageGrab
            
            if region:
                screenshot = ImageGrab.grab(bbox=region)
            else:
                screenshot = ImageGrab.grab()
            
            # Convert to bytes
            buffer = BytesIO()
            screenshot.save(buffer, format="PNG")
            return buffer.getvalue()
        
        except Exception as e:
            logger.error(f"Failed to capture screen: {e}")
            raise
    
    def analyze_image(self, image_data: bytes, question: str = "Describe this image in detail") -> str:
        """
        Analyze an image using AI vision.
        
        Args:
            image_data: Image as bytes
            question: Question about the image
            
        Returns:
            AI's analysis of the image
        """
        try:
            if self.provider == "openai":
                return self._analyze_openai(image_data, question)
            elif self.provider == "gemini":
                return self._analyze_gemini(image_data, question)
        except Exception as e:
            logger.error(f"Failed to analyze image: {e}")
            return f"Error analyzing image: {e}"
    
    def _analyze_openai(self, image_data: bytes, question: str) -> str:
        """Analyze image using OpenAI GPT-4 Vision."""
        # Encode image to base64
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        return response.choices[0].message.content    
    def _analyze_gemini(self, image_data: bytes, question: str) -> str:
        """Analyze image using Gemini Vision."""
        from PIL import Image
        
        # Convert bytes to PIL Image
        image = Image.open(BytesIO(image_data))
        
        response = self.client.generate_content([question, image])
        return response.text
    
    def analyze_screen(self, question: str = "What's on screen?") -> str:
        """
        Capture and analyze the current screen.
        
        Args:
            question: Question about the screen
            
        Returns:
            Analysis of the screen
        """
        logger.info(f"Analyzing screen: {question}")
        screenshot = self.capture_screen()
        return self.analyze_image(screenshot, question)
    
    def extract_text(self, image_data: bytes) -> str:
        """
        Extract text from image using OCR.
        
        Args:
            image_data: Image as bytes
            
        Returns:
            Extracted text
        """
        try:
            from PIL import Image
            import pytesseract
            
            image = Image.open(BytesIO(image_data))
            text = pytesseract.image_to_string(image)
            logger.info("OCR extraction completed")
            return text.strip()
        
        except ImportError:
            return "OCR requires pytesseract. Install: pip install pytesseract"
        except Exception as e:
            logger.error(f"OCR failed: {e}")
            return f"Failed to extract text: {e}"
    
    def generate_image(self, prompt: str, save_path: Optional[str] = None) -> Optional[str]:
        """
        Generate an image from text prompt.
        
        Args:
            prompt: Description of image to generate
            save_path: Optional path to save image
            
        Returns:
            Path to generated image or URL
        """
        try:
            if self.provider == "openai":
                return self._generate_openai(prompt, save_path)
            else:
                return "Image generation only supported with OpenAI provider"
        except Exception as e:
            logger.error(f"Image generation failed: {e}")
            return f"Error: {e}"
    
    def _generate_openai(self, prompt: str, save_path: Optional[str] = None) -> str:
        """Generate image using DALL-E."""
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        
        image_url = response.data[0].url
        
        if save_path:
            import requests
            from PIL import Image
            
            # Download and save
            img_data = requests.get(image_url).content
            image = Image.open(BytesIO(img_data))
            image.save(save_path)
            logger.info(f"Image saved to: {save_path}")
            return save_path
        
        return image_url
    
    def identify_objects(self, image_data: bytes) -> List[str]:
        """
        Identify objects in an image.
        
        Args:
            image_data: Image as bytes
            
        Returns:
            List of identified objects
        """
        result = self.analyze_image(
            image_data,
            "List all objects you can identify in this image. Return only a comma-separated list."
        )
        return [obj.strip() for obj in result.split(',')]


# Standalone test
if __name__ == "__main__":
    print("=== Zen AI Vision Test ===\n")
    
    try:
        vision = AIVision(provider="openai")
        
        print("1. Testing screen capture...")
        screenshot = vision.capture_screen()
        print(f"✓ Captured {len(screenshot)} bytes\n")
        
        print("2. Testing screen analysis...")
        # This requires API key
        # analysis = vision.analyze_screen("What applications are visible?")
        # print(f"Analysis: {analysis}\n")
        
        print("Note: Full vision features require:")
        print("  - OpenAI API key with GPT-4 Vision access")
        print("  - OR Google Gemini Pro Vision API key")
        
        print("\n✓ AI Vision module ready!")
    
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure API keys are configured in .env")
