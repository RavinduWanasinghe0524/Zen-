"""
Zen Voice Assistant - Theme System
Futuristic visual themes with dynamic color schemes.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class Theme:
    """Theme configuration for neural GUI."""
    name: str
    primary: str
    secondary: str
    accent: str
    bg: str
    glow: str
    text: str = "#FFFFFF"
    description: str = ""


class ThemeManager:
    """Manages visual themes for the assistant."""
    
    # Predefined futuristic themes
    THEMES = {
        "cyber_blue": Theme(
            name="Cyber Blue",
            primary="#00F0FF",
            secondary="#0080FF",
            accent="#00FFAA",
            bg="#0A0E1A",
            glow="#00F0FF",
            description="Matrix-inspired cyan and blue cyberpunk theme"
        ),
        
        "neural_purple": Theme(
            name="Neural Purple",
            primary="#B026FF",
            secondary="#FF10F0",
            accent="#FFB6C1",
            bg="#1A0A1E",
            glow="#FF10F0",
            description="Deep purple with pink accents, neural aesthetic"
        ),
        
        "quantum_orange": Theme(
            name="Quantum Orange",
            primary="#FF8C00",
            secondary="#FFD700",
            accent="#FFA500",
            bg="#1A1410",
            glow="#FFD700",
            description="Warm orange and gold energy theme"
        ),
        
        "dark_matter": Theme(
            name="Dark Matter",
            primary="#FFFFFF",
            secondary="#00FFFF",
            accent="#FF00FF",
            bg="#000000",
            glow="#00FFFF",
            description="Pure black with bright white and neon accents"
        ),
        
        "neon_pink": Theme(
            name="Neon Pink",
            primary="#FF006E",
            secondary="#FB5607",
            accent="#FFBE0B",
            bg="#1A0514",
            glow="#FF006E",
            description="Vibrant pink and orange neon lights"
        ),
        
        "arctic_ice": Theme(
            name="Arctic Ice",
            primary="#E0FFFF",
            secondary="#87CEEB",
            accent="#B0E0E6",
            bg="#0F1419",
            glow="#E0FFFF",
            description="Cool ice blue and white theme"
        ),
        
        "toxic_green": Theme(
            name="Toxic Green",
            primary="#39FF14",
            secondary="#00FF00",
            accent="#ADFF2F",
            bg="#0A140A",
            glow="#39FF14",
            description="Radioactive green sci-fi theme"
        ),
        
        "sunset_gradient": Theme(
            name="Sunset Gradient",
            primary="#FF6B6B",
            secondary="#FFE66D",
            accent="#4ECDC4",
            bg="#1A1414",
            glow="#FF6B6B",
            description="Warm sunset colors with turquoise accent"
        )
    }
    
    @classmethod
    def get_theme(cls, theme_name: str) -> Theme:
        """Get theme by name."""
        return cls.THEMES.get(theme_name, cls.THEMES["cyber_blue"])
    
    @classmethod
    def list_themes(cls) -> Dict[str, str]:
        """List all available themes with descriptions."""
        return {name: theme.description for name, theme in cls.THEMES.items()}
    
    @classmethod
    def create_custom_theme(cls, name: str, primary: str, secondary: str, 
                           accent: str, bg: str, glow: str) -> Theme:
        """Create a custom theme."""
        return Theme(
            name=name,
            primary=primary,
            secondary=secondary,
            accent=accent,
            bg=bg,
            glow=glow,
            description="Custom user-created theme"
        )


# Test
if __name__ == "__main__":
    print("=== Zen Theme System ===\n")
    print("Available Themes:\n")
    
    for name, description in ThemeManager.list_themes().items():
        theme = ThemeManager.get_theme(name)
        print(f"📐 {theme.name}")
        print(f"   {description}")
        print(f"   Colors: {theme.primary} | {theme.secondary} | {theme.accent}\n")
    
    print("\n✓ Theme system ready!")
