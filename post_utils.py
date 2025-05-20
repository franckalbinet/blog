from pathlib import Path
import yaml
from datetime import datetime
import re
from typing import List, Optional

class Post:
    def __init__(self, title: str, summary: str, date: str, tags: List[str], content: str, slug: str):
        self.title = title
        self.summary = summary
        self.date = date
        self.tags = tags
        self.content = content
        self.slug = slug

    @classmethod
    def from_markdown(cls, file_path: Path) -> 'Post':
        """Create a Post instance from a markdown file with YAML frontmatter."""
        content = file_path.read_text()
        
        # Split the frontmatter from the content
        pattern = r'^---\n(.*?)\n---\n(.*)'
        match = re.match(pattern, content, re.DOTALL)
        
        if not match:
            raise ValueError(f"Invalid markdown file format in {file_path}")
            
        frontmatter, content = match.groups()
        
        # Parse YAML frontmatter
        metadata = yaml.safe_load(frontmatter)
        
        # Generate slug from filename
        slug = file_path.stem
        
        # Add heading anchors to the content
        content = add_heading_anchors(content.strip())
        
        return cls(
            title=metadata['title'],
            summary=metadata['summary'],
            date=metadata['date'],
            tags=metadata['tags'],
            content=content,
            slug=slug
        )

def load_posts(posts_dir: str) -> List[Post]:
    """Load all markdown posts from the specified directory."""
    posts_path = Path(posts_dir)
    if not posts_path.exists():
        raise FileNotFoundError(f"Posts directory not found: {posts_dir}")
        
    posts = []
    for file_path in posts_path.glob('*.md'):
        try:
            post = Post.from_markdown(file_path)
            posts.append(post)
        except Exception as e:
            print(f"Error loading post {file_path}: {e}")
            
    # Sort posts by date (newest first)
    return sorted(posts, key=lambda x: x.date, reverse=True)

def add_heading_anchors(content: str) -> str:
    """Add anchor elements before each h2 heading in markdown content."""
    lines = content.split('\n')
    processed_lines = []
    
    for line in lines:
        if line.startswith('## '):
            # Extract the heading text
            heading = line[3:].strip()
            # Create the anchor ID
            anchor = heading.lower().replace(' ', '-')
            # Add the anchor element before the heading
            processed_lines.append(f'<a id="{anchor}"></a>')
        processed_lines.append(line)
    
    return '\n'.join(processed_lines) 