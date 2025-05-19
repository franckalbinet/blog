from fasthtml.common import *
from monsterui.all import *

def SocialLink(icon, text, url):
    """Creates a social media link with icon"""
    return A(
        DivLAligned(
            UkIcon(icon),
            P(text, cls=TextPresets.md_weight_sm)
        ),
        href=url,
        target="_blank",
        rel="noopener noreferrer",
        cls="hover:text-gray-500 duration-200"
    )
