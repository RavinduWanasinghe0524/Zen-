"""
Zen Voice Assistant - App Control Module
Specialized control for media apps like Spotify and YouTube.
"""

import logging
import webbrowser
import time
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

logger = logging.getLogger(__name__)

class AppController:
    """Controls external applications."""
    
    @staticmethod
    def control_media(action: str) -> str:
        """
        Control system media playback (Spotify, YouTube, etc.).
        
        Args:
            action: 'play', 'pause', 'next', 'previous', 'volume_up', 'volume_down'
            
        Returns:
            Status message
        """
        if not PYAUTOGUI_AVAILABLE:
            return "Media control requires pyautogui. Install: pip install pyautogui"
        
        try:
            if action in ['play', 'pause']:
                pyautogui.press('playpause')
            elif action == 'next':
                pyautogui.press('nexttrack')
            elif action == 'previous':
                pyautogui.press('prevtrack')
            elif action == 'volume_up':
                pyautogui.press('volumeup')
            elif action == 'volume_down':
                pyautogui.press('volumedown')
            elif action == 'mute':
                pyautogui.press('volumemute')
            else:
                return f"Unknown media action: {action}"
                
            logger.info(f"Media action: {action}")
            return f"Executed media command: {action}"
            
        except Exception as e:
            logger.error(f"Failed to control media: {e}")
            return f"Error controlling media: {e}"

    @staticmethod
    def play_on_youtube(query: str) -> str:
        """
        Search and play video on YouTube.
        
        Args:
            query: Video search query
            
        Returns:
            Status message
        """
        try:
            # Create search URL
            search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            
            # Note: For full automation we'd need more complex logic, 
            # but opening the search results is a good start.
            # Using pyautogui to click the first video is risky without vision.
            # We'll just open the results for now.
            
            logger.info(f"YouTube search: {query}")
            return f"Opening YouTube results for {query}."
            
        except Exception as e:
            logger.error(f"Failed to play YouTube: {e}")
            return f"Error playing YouTube: {e}"

# Standalone Test
if __name__ == "__main__":
    print("=== App Control Test ===\n")
    
    if not PYAUTOGUI_AVAILABLE:
        print("x pyautogui not installed. Please install it.")
    else:
        print("Testing volume (should change volume)...")
        AppController.control_media("volume_up")
        time.sleep(1)
        AppController.control_media("volume_down")
        print("✓ Volume test done")
        
        # print("Testing YouTube...")
        # AppController.play_on_youtube("funny cats")
