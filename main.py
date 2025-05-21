from fasthtml.common import *
from monsterui.all import *
# from fh_posts.all import *
from pathlib import Path
from post_utils import *
from ui_components import *

# App setup
app, rt = fast_app(
    title="Franck Albinet's blog",
    hdrs=Theme.slate.headers(mode="light", radii="small"),
    live=True
)

def layout(content, active_route="/"):
    """Wrap content in consistent page layout with navigation."""
    return Div(
        Navbar(active_route), 
        Container(content), 
        cls="lg:mx-10 xl:mx-20"  # Responsive margins
    )

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
                ),
                cls="gap-x-2 items-center mt-5"
            )
        )
    )

def post_links(posts):
    return [
        A(
            Div(
                H5(post.title, cls="hover:underline"),
                P(post.summary, cls="text-sm"),
                DivHStacked(
                    P(post.date, cls=TextT.muted + "text-sm"),
                    P(" - "),   
                    P(", ".join(post.tags), cls=TextT.muted + "text-sm"),
                    cls="gap-x-2"
                ),
                cls="mb-4"
            ),
            href=f"/post/{post.slug}"
        )
        for post in posts
    ]

@rt('/')
def get():
    # Load posts on each request
    posts = [o for o in load_posts('posts') if not o.slug.startswith('_')]
        
    return layout(
        Div(
            H1("Index", cls="mb-10" + TextT.light),
            Div(*post_links(posts)),
            cls="space-y-4 mt-5"
        ),
        active_route="/"
    )

@rt('/about')
def about(): 
    bio = Path("about.md").read_text()
    return layout(
        Div(
            H1("About me", cls="mb-10" + TextT.light),
            Grid(
                # Left column - Personal info (1/3)
                Div(
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
                            P("Geospatial Analysis"),
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
                        cls="p-6 gap-y-4"
                    ),
                    cls="col-span-4 hidden md:block pt-20"  # Changed from col-span-3 to col-span-4 (1/3 of 12)
                ),
                # Right column - Bio (2/3)
                Div(
                    render_md(bio, class_map_mods={'p': TextT.lg + "mb-5"}),
                    cls="col-span-8 p-6"  # Changed from col-span-9 to col-span-8 (2/3 of 12)
                ),
                cols_sm=1,     # 1 column on small screens
                cols_md=12,    # 12-column grid on medium screens
                cols_lg=12,    # 12-column grid on large screens
                cols_xl=12,    # 12-column grid on extra large screens
                cls="mt-5"
            ),
            cls="mt-5"
        ),
        active_route="/about"
    )

@rt("/post/{post_slug}")
def get(post_slug: str):
    # Load posts on each request
    posts = load_posts('posts')
    
    # Find the post or return 404
    post = next((p for p in posts if p.slug == post_slug and not p.slug.startswith('_')), None) 
    
    # Extract headings for TOC
    headings = []
    for line in post.content.split('\n'):
        if line.startswith('## '):
            heading = line[3:].strip()
            anchor = heading.lower().replace(' ', '-')
            headings.append((heading, anchor))
                
    # Calculate reading time (rough estimate: 200 words per minute)
    word_count = len(post.content.split())
    reading_time = max(1, round(word_count / 200))
    
    # Create scrollspy navigation links
    scrollspy_links = [A(heading, href=f"#{anchor}") for heading, anchor in headings]
    
    return layout(
        Grid(
            Div(
                DivVStacked(
                    P(post.date, cls=TextT.muted),
                    P(f"{reading_time} min read", cls=TextT.muted),
                    # Add code link if available in post metadata
                    *([A("View Code", href=post.code_url, cls="text-blue-600 hover:underline")] 
                      if hasattr(post, 'code_url') else []),
                    cls="gap-y-1"
                ),
                cls="col-span-2 hidden md:block pt-60"
            ),
            Div(
                Div(
                    H2(post.title, cls="mb-5 hover:underline" + TextT.light),
                    H4(post.summary, cls=TextT.muted + TextT.light),
                    cls="mb-10"
                ),
                render_md(post.content, class_map_mods={
                    'p': TextT.lg +  "mb-5 mt-2",
                    'h2': "scroll-mt-20" + TextT.bold + TextT.lg,
                    "figcaption": TextT.center
                }),
                cls="col-span-7 p-4"
            ),
            Div(
                NavContainer(
                    *map(Li, scrollspy_links),
                    uk_scrollspy_nav=True,
                    sticky=True,
                    cls=(NavT.default, "top-20")
                ),
                cls="col-span-3 hidden md:block p-4 sticky top-10 pt-60"
            ),
            cols_sm=1,     # 1 column on small screens
            cols_md=12,    # 12-column grid on medium screens
            cols_lg=12,    # 12-column grid on large screens
            cols_xl=12,    # 12-column grid on extra large screens
            cls="mt-10"
            
            
        ),
        active_route=f"/posts/{post_slug}"
    )


from starlette.responses import FileResponse

@rt("/static/{path:path}")
async def static_files(path: str):
    return FileResponse(f"static/{path}")

serve()