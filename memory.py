"""
Zen Voice Assistant - Long-Term Memory Module
Stores and retrieves user facts using a simple JSON database.
"""

import json
import os
import logging
from datetime import datetime
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class ZenMemory:
    """Simple JSON-based long-term memory system."""
    
    def __init__(self, memory_file: str = "brain_data/memory.json"):
        """
        Initialize memory system.
        
        Args:
            memory_file: Path to JSON storage file
        """
        self.memory_file = memory_file
        self.memories = []
        self._ensure_directory()
        self._load_memory()
    
    def _ensure_directory(self):
        """Ensure the storage directory exists."""
        directory = os.path.dirname(self.memory_file)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
    def _load_memory(self):
        """Load memories from file."""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.memories = data.get('memories', [])
                logger.info(f"Loaded {len(self.memories)} memories")
            else:
                self.memories = []
                self._save_memory()
        except Exception as e:
            logger.error(f"Failed to load memory: {e}")
            self.memories = []

    def _save_memory(self):
        """Save memories to file."""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'last_updated': datetime.now().isoformat(),
                    'memories': self.memories
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save memory: {e}")

    def remember(self, text: str, tags: List[str] = None) -> Dict:
        """
        Store a new memory.
        
        Args:
            text: The fact/info to remember
            tags: Optional tags for categorization
            
        Returns:
            The created memory object
        """
        memory = {
            'id': len(self.memories) + 1,
            'text': text,
            'tags': tags or [],
            'created_at': datetime.now().isoformat()
        }
        
        self.memories.append(memory)
        self._save_memory()
        logger.info(f"Remembered: {text[:30]}...")
        return memory

    def recall(self, query: str, limit: int = 3) -> List[Dict]:
        """
        Retrieve relevant memories based on keyword matching.
        
        Args:
            query: The search query
            limit: Max number of results
            
        Returns:
            List of matching memories
        """
        query_words = set(query.lower().split())
        scored_memories = []
        
        for mem in self.memories:
            # Simple keyword matching score
            text_words = set(mem['text'].lower().split())
            score = len(query_words.intersection(text_words))
            
            if score > 0:
                scored_memories.append((score, mem))
        
        # Sort by score descending
        scored_memories.sort(key=lambda x: x[0], reverse=True)
        
        return [m[1] for m in scored_memories[:limit]]

    def get_all_memories(self) -> List[Dict]:
        """Get all stored memories."""
        return self.memories

    def clear_memory(self):
        """Wipe all memories."""
        self.memories = []
        self._save_memory()

# Standalone Test
if __name__ == "__main__":
    print("=== Zen Memory Test ===\n")
    
    brain = ZenMemory("test_memory.json")
    
    # Test Remember
    print("Storing memories...")
    brain.remember("My name is Stark", ["user_info"])
    brain.remember("I like pepperoni pizza", ["preferences"])
    brain.remember("My wifi password is 'galaxy123'", ["security"])
    
    # Test Recall
    print("\nRecalling 'pizza':")
    results = brain.recall("Do inside like pizza?")
    for res in results:
        print(f" - {res['text']}")
        
    print("\nRecalling 'name':")
    results = brain.recall("What is my name?")
    for res in results:
        print(f" - {res['text']}")
    
    # Cleanup
    if os.path.exists("test_memory.json"):
        os.remove("test_memory.json")
    print("\n[Done] Test complete")
