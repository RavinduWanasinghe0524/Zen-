"""
Zen Voice Assistant - AI Brain Module
Handles AI integration and conversation management.
"""

import logging
import json
from typing import List, Dict, Optional, Callable
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIBrain:
    """Manages AI interactions, conversation context, and tool-use."""
    
    def __init__(self):
        """Initialize the AI brain with the configured provider."""
        self.provider = Config.AI_PROVIDER
        self.conversation_history = []
        self.tools = {}
        self.tool_functions = {}
        self.client = None
        # Note: Provider is initialized after tools are registered.
    
    def _initialize_provider(self):
        """Initialize the selected AI provider with registered tools."""
        try:
            if self.provider == "openai":
                self._initialize_openai()
            elif self.provider == "gemini":
                self._initialize_gemini()
            elif self.provider == "ollama":
                self._initialize_ollama()
            else:
                raise ValueError(f"Unsupported AI provider: {self.provider}")
            
            # Add system prompt to history
            self.conversation_history.append(
                {"role": "system", "content": Config.SYSTEM_PROMPT}
            )
            logger.info(f"AI Brain initialized with provider: {self.provider}")
            
        except Exception as e:
            logger.error(f"Failed to initialize AI provider: {e}")
            raise
    
    def _initialize_openai(self):
        """Initialize OpenAI client."""
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
            self.model = "gpt-4o-mini"
            logger.info("OpenAI client initialized")
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
    
    def _initialize_gemini(self):
        """Initialize Google Gemini client with tools."""
        try:
            import google.generativeai as genai
            genai.configure(api_key=Config.GEMINI_API_KEY)
            
            # Convert our tool format to Gemini's format
            gemini_tools = []
            for name, details in self.tools.items():
                gemini_tools.append({
                    "name": name,
                    "description": details["description"],
                    "parameters": details["parameters"]
                })

            self.client = genai.GenerativeModel(
                'gemini-1.5-flash',
                tools=gemini_tools
            )
            self.chat_session = self.client.start_chat(enable_automatic_function_calling=True)
            logger.info(f"Gemini client initialized with {len(gemini_tools)} tools.")
        except ImportError:
            raise ImportError("google-generativeai package not installed. Run: pip install google-generativeai")
    
    def _initialize_ollama(self):
        """Initialize Ollama client."""
        try:
            import ollama
            self.client = ollama
            self.model = Config.OLLAMA_MODEL
            logger.info(f"Ollama client initialized with model: {self.model}")
        except ImportError:
            raise ImportError("ollama package not installed. Run: pip install ollama")

    def register_tool(self, name: str, description: str, function: Callable, parameters: Dict):
        """
        Register a tool/function that the AI can call.
        
        Args:
            name: Function name
            description: What the function does
            function: The callable function
            parameters: JSON schema for function parameters
        """
        self.tools[name] = {
            "description": description,
            "parameters": parameters
        }
        self.tool_functions[name] = function
        logger.info(f"Registered tool: {name}")

    def finish_initialization(self):
        """Finalize initialization after all tools are registered."""
        self._initialize_provider()

    def get_response(self, user_input: str) -> Dict:
        """
        Get AI response for user input, handling tool calls.
        
        Args:
            user_input: User's message
            
        Returns:
            Dict with 'type' ('text' or 'tool_call') and 'content'
        """
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        try:
            if self.provider == "gemini":
                response = self._get_gemini_response(user_input)
            elif self.provider == "openai":
                response = self._get_openai_response(user_input)
            elif self.provider == "ollama":
                response = self._get_ollama_response(user_input)
            else:
                response = {"type": "text", "content": "AI provider not configured."}
            
            # Add assistant response to history if it's pure text
            if response["type"] == "text":
                self.conversation_history.append({"role": "assistant", "content": response["content"]})
            
            self._trim_history()
            return response
            
        except Exception as e:
            logger.error(f"Error getting AI response: {e}", exc_info=True)
            return {"type": "text", "content": "I'm having trouble processing that. Could you try again?"}

    def _get_gemini_response(self, user_input: str) -> Dict:
        """Get response from Google Gemini, handling function calls."""
        from google.generativeai.types import FunctionCall
        
        response = self.chat_session.send_message(user_input)
        
        if not response.parts:
             return {"type": "text", "content": "I apologize, I could not generate a response."}

        # Check for function call
        if response.parts[0].function_call:
            fc = response.parts[0].function_call
            tool_name = fc.name
            tool_args = fc.args
            
            if tool_name in self.tool_functions:
                logger.info(f"AI requested tool '{tool_name}' with args: {tool_args}")
                
                # Execute the tool function
                tool_function = self.tool_functions[tool_name]
                try:
                    # Use ** to unpack dict into keyword arguments
                    result = tool_function(**tool_args)
                    logger.info(f"Tool '{tool_name}' executed, result: {result}")
                    # The automatic function calling will handle sending this back
                    return {"type": "tool_call", "content": result}
                except Exception as e:
                    logger.error(f"Error executing tool {tool_name}: {e}")
                    return {"type": "text", "content": f"I failed to use the tool {tool_name}."}
            else:
                logger.warning(f"AI requested unknown tool: {tool_name}")
                return {"type": "text", "content": f"I tried to use a tool named {tool_name}, but I don't have it."}
        
        # If no function call, just return the text
        return {"type": "text", "content": response.text}

    def _get_openai_response(self, user_input: str) -> Dict:
        """Get response from OpenAI."""
        # This part needs to be updated to support tool calling similar to Gemini's
        messages = [{"role": msg["role"], "content": msg["content"]} 
                   for msg in self.conversation_history]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        
        content = response.choices[0].message.content
        return {"type": "text", "content": content}

    def _get_ollama_response(self, user_input: str) -> Dict:
        """Get response from Ollama."""
        # Ollama support for tool-calling is limited and requires specific model fine-tuning.
        messages = [{"role": msg["role"], "content": msg["content"]} 
                   for msg in self.conversation_history if msg["role"] != "system"]
        
        response = self.client.chat(model=self.model, messages=messages)
        content = response['message']['content']
        return {"type": "text", "content": content}

    def _trim_history(self):
        """Trim conversation history to prevent token overflow."""
        if len(self.conversation_history) > Config.MAX_HISTORY_LENGTH + 1:
            system_prompt = self.conversation_history[0]
            recent_messages = self.conversation_history[-(Config.MAX_HISTORY_LENGTH):]
            self.conversation_history = [system_prompt] + recent_messages
    
    def clear_history(self):
        """Clear conversation history (keep system prompt)."""
        system_prompt = self.conversation_history[0] if self.conversation_history else None
        self.conversation_history = [system_prompt] if system_prompt else []
        if self.provider == "gemini":
            # Re-initialize chat session to clear remote history
            self._initialize_gemini()


# Standalone test
if __name__ == "__main__":
    print("=== Zen AI Brain Test ===")
    
    try:
        brain = AIBrain()
        
        # Test conversation
        test_inputs = [
            "Hello, what's your name?",
            "Tell me a fun fact about space.",
            "What's 25 times 4?"
        ]
        
        for user_input in test_inputs:
            print(f"\nUser: {user_input}")
            response = brain.get_response(user_input)
            print(f"Zen: {response['content']}")
        
        print("\n✓ AI Brain test complete!")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure you have:")
        print("1. Created a .env file (run: python config.py)")
        print("2. Added your API key to the .env file")
        print("3. Installed required packages (pip install -r requirements.txt)")
