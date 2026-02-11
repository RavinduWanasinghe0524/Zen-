"""
Zen Voice Assistant - OS Automation Tools
Windows-specific automation functions.
"""

import os
import subprocess
import webbrowser
import logging
from datetime import datetime
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


from memory import ZenMemory
from app_control import AppController
from research import ZenResearcher

class ZenTools:
    """Collection of OS automation tools for Zen."""
    
    def __init__(self):
        self.memory = ZenMemory()
        self.app_controller = AppController()
        self.researcher = ZenResearcher()
    
    def remember_fact(self, fact: str) -> str:
        """
        Store a fact or piece of information in long-term memory.
        
        Args:
            fact: The information to remember
            
        Returns:
            Confirmation message
        """
        self.memory.remember(fact)
        return "I've stored that in my official memory."

    def recall_memories(self, query: str) -> str:
        """
        Search long-term memory for information.
        
        Args:
            query: The topic or question to search for
            
        Returns:
            Combined string of matching memories
        """
        results = self.memory.recall(query, limit=3)
        if results:
            memories = "\n".join([f"- {r['text']}" for r in results])
            return f"Here is what I found in my memory:\n{memories}"
        return "I couldn't find any relevant memories about that."

    def research_topic(self, query: str) -> str:
        """
        Research a topic by searching the web and summarizing results.
        
        Args:
            query: The topic to research
            
        Returns:
            Summary of research findings
        """
        return self.researcher.search_and_summarize(query)

    def control_media(self, action: str) -> str:
        """
        Control music or video playback.
        
        Args:
            action: 'play', 'pause', 'next', 'previous', 'volume_up', 'volume_down'
            
        Returns:
            Status message
        """
        return self.app_controller.control_media(action)

    def play_youtube(self, query: str) -> str:
        """
        Search and play a video on YouTube.
        
        Args:
            query: The video to search for
            
        Returns:
            Status message
        """
        return self.app_controller.play_on_youtube(query)

    @staticmethod
    def open_application(app_name: str) -> str:
        """
        Open a Windows application.
        
        Args:
            app_name: Name of the application (e.g., "notepad", "chrome", "calculator")
            
        Returns:
            Status message
        """
        app_name_lower = app_name.lower()
        
        # Map common app names to executable commands
        app_map = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "chrome": "chrome.exe",
            "firefox": "firefox.exe",
            "edge": "msedge.exe",
            "explorer": "explorer.exe",
            "cmd": "cmd.exe",
            "powershell": "powershell.exe",
            "task manager": "taskmgr.exe",
            "control panel": "control.exe",
            "settings": "ms-settings:",
        }
        
        try:
            if app_name_lower in app_map:
                command = app_map[app_name_lower]
                if command.startswith("ms-"):
                    os.system(f'start {command}')
                else:
                    subprocess.Popen(command, shell=True)
                logger.info(f"Opened application: {app_name}")
                return f"Opened {app_name} successfully."
            else:
                # Try to open as generic application
                subprocess.Popen(app_name, shell=True)
                return f"Attempting to open {app_name}."
                
        except Exception as e:
            logger.error(f"Failed to open {app_name}: {e}")
            return f"Sorry, I couldn't open {app_name}."
    
    @staticmethod
    def get_current_time() -> str:
        """
        Get the current date and time.
        
        Returns:
            Formatted date and time string
        """
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        date_str = now.strftime("%A, %B %d, %Y")
        return f"It's {time_str} on {date_str}."
    
    @staticmethod
    def search_web(query: str) -> str:
        """
        Search the web using the default browser.
        
        Args:
            query: Search query
            
        Returns:
            Status message
        """
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            logger.info(f"Web search: {query}")
            return f"Searching the web for {query}."
        except Exception as e:
            logger.error(f"Failed to search web: {e}")
            return "Sorry, I couldn't open the web browser."
    
    @staticmethod
    def get_system_info() -> str:
        """
        Get basic system information.
        
        Returns:
            System information string
        """
        try:
            import platform
            import psutil
            
            system = platform.system()
            version = platform.version()
            processor = platform.processor()
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            info = (
                f"System: {system}, "
                f"CPU usage: {cpu_percent}%, "
                f"Memory usage: {memory_percent}%"
            )
            return info
            
        except ImportError:
            return "System information requires psutil package. Install with: pip install psutil"
        except Exception as e:
            logger.error(f"Failed to get system info: {e}")
            return "Sorry, I couldn't retrieve system information."
    
    @staticmethod
    def set_volume(level: int) -> str:
        """
        Set system volume (Windows only).
        
        Args:
            level: Volume level (0-100)
            
        Returns:
            Status message
        """
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            # Set volume (0.0 to 1.0)
            volume_level = max(0, min(100, level)) / 100.0
            volume.SetMasterVolumeLevelScalar(volume_level, None)
            
            logger.info(f"Set volume to {level}%")
            return f"Volume set to {level} percent."
            
        except ImportError:
            return "Volume control requires pycaw package. Install with: pip install pycaw comtypes"
        except Exception as e:
            logger.error(f"Failed to set volume: {e}")
            return "Sorry, I couldn't adjust the volume."
    
    @staticmethod
    def shutdown_system(confirm: bool = True) -> str:
        """
        Shutdown the system.
        
        Args:
            confirm: Whether confirmation is required
            
        Returns:
            Status message
        """
        if not confirm:
            return "Shutdown cancelled."
        
        try:
            logger.info("Initiating system shutdown...")
            os.system("shutdown /s /t 30")
            return "Shutting down in 30 seconds. To cancel, run: shutdown /a"
        except Exception as e:
            logger.error(f"Failed to shutdown: {e}")
            return "Sorry, I couldn't shutdown the system."
    
    @staticmethod
    def restart_system(confirm: bool = True) -> str:
        """
        Restart the system.
        
        Args:
            confirm: Whether confirmation is required
            
        Returns:
            Status message
        """
        if not confirm:
            return "Restart cancelled."
        
        try:
            logger.info("Initiating system restart...")
            os.system("shutdown /r /t 30")
            return "Restarting in 30 seconds. To cancel, run: shutdown /a"
        except Exception as e:
            logger.error(f"Failed to restart: {e}")
            return "Sorry, I couldn't restart the system."


# Standalone test
if __name__ == "__main__":
    print("=== Zen Tools Test ===\n")
    
    tools = ZenTools()
    
    # Test get time
    print(f"Time: {tools.get_current_time()}\n")
    
    # Test system info
    print(f"System: {tools.get_system_info()}\n")
    
    # Test open application (safe test)
    print("Opening Notepad...")
    print(tools.open_application("notepad"))
    
    print("\n✓ Tools test complete!")
