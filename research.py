"""
Zen Voice Assistant - Research Module
Enables "Agent Mode" by performing deep web research and summarization.
"""

import logging
import requests
from bs4 import BeautifulSoup
try:
    from googlesearch import search
except ImportError:
    search = None

logger = logging.getLogger(__name__)

class ZenResearcher:
    """Handles web research and content extraction."""
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def search_and_summarize(self, query: str, num_results: int = 3) -> str:
        """
        Perform a Google search, read top results, and summarize.
        
        Args:
            query: Search query
            num_results: Number of pages to analyze
            
        Returns:
            Summary of findings
        """
        if not search:
            return "Research module requires googlesearch-python. Install: pip install googlesearch-python"

        try:
            logger.info(f"Researching: {query}")
            urls = list(search(query, num_results=num_results, advanced=True))
            
            summary = [f"Research results for '{query}':\n"]
            
            for i, result in enumerate(urls[:num_results]):
                try:
                    url = result.url
                    title = result.title
                    description = result.description
                    
                    logger.info(f"Reading: {url}")
                    # Basic content extraction
                    content = self._fetch_page_content(url)
                    
                    summary.append(f"Source {i+1}: {title}")
                    summary.append(f"URL: {url}")
                    summary.append(f"Snippet: {description}")
                    summary.append(f"Content Preview: {content[:500]}...\n")
                    
                except Exception as e:
                    logger.warning(f"Failed to read {url}: {e}")
                    continue
            
            combined_summary = "\n".join(summary)
            return combined_summary
            
        except Exception as e:
            logger.error(f"Research failed: {e}")
            return f"I encountered an error while researching: {e}"

    def _fetch_page_content(self, url: str) -> str:
        """Fetch and clean text from a URL."""
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove scripts and styles
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.extract()
                
            # Get text
            text = soup.get_text()
            
            # Clean lines
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
            
        except Exception as e:
            return f"[Error extracting content: {e}]"

# Standalone Test
if __name__ == "__main__":
    print("=== Zen Research Test ===\n")
    if not search:
        print("x googlesearch-python not installed")
    else:
        researcher = ZenResearcher()
        print("Researching 'latest spacex launch'...")
        result = researcher.search_and_summarize("latest spacex launch", num_results=1)
        print(f"\nResult:\n{result[:500]}...")
