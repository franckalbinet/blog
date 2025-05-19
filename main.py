from fasthtml.common import *
from monsterui.all import *
from fh_posts.all import *
from pathlib import Path
from ui_components import *

# App setup
app, rt = fast_app(
    title="Franck Albinet's blog",
    hdrs=Theme.slate.headers(mode="light", radii="small"),
    static_path="static",
    live=True
)


def layout(content, active_route="/"):
    """Wrap content in consistent page layout with navigation."""
    return Div(Navbar(active_route), Container(content), cls="ml-20 mr-20")

def Navbar(active_route="/"):
    """Create a consistent navbar with active route highlighting"""
    links = [
        A("BLOG", href='/', cls=TextT.muted + " hover:text-gray-800" if active_route != "/" else ""),    
        # A("PROJECTS", href='/projects', cls=TextT.muted + " hover:text-gray-500" if active_route != "/projects" else ""),    
        A("ABOUT ME", href='/about', cls=TextT.muted + " hover:text-gray-800" if active_route != "/about" else ""),
    ]
    return NavBar(
        DivHStacked(
            *links,
            cls="gap-x-10" + TextT.medium
        ),
        brand=Div(
            DivHStacked(
                Div(
                    "F",
                    cls="w-6 h-6 rounded-full bg-gray-700 text-white flex items-center justify-center text-lg font-medium"
                ),
                A(
                    'FR.ANCKALBI.NET', 
                    href="/",
                    cls=TextT.medium
                    # cls=TextT.lg + TextT.gray + TextT.medium
                ),
                cls="gap-x-2 items-center"
            )
        )
    )



@rt('/')
def get():
    return layout(
        Div(
            H1("Index", cls="mb-10" + TextT.light),
            Div(
                Div(
                    A("Getting Started with FastHTML", href="/posts/getting-started", cls=TextT.medium),
                    P("March 15, 2024", cls=TextT.muted + "text-sm"),
                    cls="mb-4"
                ),
                Div(
                    A("Building a Modern Blog", href="/posts/modern-blog", cls=TextT.medium),
                    P("March 10, 2024", cls=TextT.muted + "text-sm"),
                    cls="mb-4"
                ),
                Div(
                    A("Web Development Tips", href="/posts/web-dev-tips", cls=TextT.medium),
                    P("March 5, 2024", cls=TextT.muted + "text-sm"),
                    cls="mb-4"
                ),
                cls="space-y-4"
            ),
            cls="mt-5"
        ),
        active_route="/")

@rt('/about')
def about(): 
    bio = Path("about.md").read_text()
    return layout(
        Div(
            H1("About me", cls="mb-10" + TextT.light),
            DivHStacked(
                # Left column - Personal info
                DivVStacked(
                    DivVStacked(
                        H3("Franck Albinet", cls=TextT.bold),
                        P("Data Science & AI Consultant", cls=TextT.muted),
                        cls="gap-2"
                    ),
                    Divider(cls=DividerT.sm),
                    DivVStacked(
                        H3("Location", cls=TextT.medium + TextT.bold),
                        P("Guéthary, France", cls=TextT.muted),
                        cls="gap-2"
                    ),
                    Divider(cls=DividerT.sm),   
                    DivVStacked(
                        H3("Areas of Expertise", cls=TextT.medium + TextT.bold),
                        P("Data Science & AI"),
                        P("Geospatial Intelligence"),
                        P("Nuclear Emergency Management"),
                        P("Humanitarian Response"),
                        cls="gap-2"
                    ),
                    Divider(cls=DividerT.sm),
                    H3("Connect", cls=TextT.medium + TextT.bold),
                    DivHStacked(
                        DivVStacked(
                            SocialLink("linkedin", "LinkedIn", "https://linkedin.com/in/franckalbinet"),
                            SocialLink("github", "GitHub", "https://github.com/franckalbinet"),
                            cls="gap-2"
                        ),
                        DivVStacked(
                            SocialLink("cloud", "BlueSky", "https://bsky.app/profile/francobollo.bsky.social"),
                            SocialLink("mail", "Email", "mailto:franckalbinet@gmail.com"),
                            cls="gap-2"
                        ),
                        cls="gap-2"
                    ),
                    cls="w-1/3 p-6 gap-y-4"
                ),
                # Right column - Bio
                Div(
                    render_md(bio, class_map_mods={'p': TextT.medium + "mb-5"}),
                    cls="w-2/3 p-6 gap-y-4"
                ),
                cls="gap-y-8"
            ),
            cls="mt-5"
        ),
        active_route="/about"
    )

serve(port=5002)