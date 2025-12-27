#!/usr/bin/env python3
"""
VERSE-STORYPATH PIPELINE
Automate the creation of narrative ML lessons with EmberMovie animations.

Usage:
    ./verse.py create --url URL --lesson NUMBER --title "Title"
    ./verse.py add-image --lesson NUMBER --image PATH
    ./verse.py generate-movie --lesson NUMBER
    ./verse.py publish --lesson NUMBER
    ./verse.py full --url URL --lesson NUMBER --title "Title" --image PATH
"""

import argparse
import os
import re
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

# Try to import optional dependencies
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_SCRAPING = True
except ImportError:
    HAS_SCRAPING = False

# Paths
REPO_ROOT = Path(__file__).parent.parent
LESSONS_DIR = REPO_ROOT / "lessons"
IMAGES_DIR = REPO_ROOT / "images"
TEMPLATES_DIR = REPO_ROOT / "templates"

# EmberMovie colors
COLORS = {
    'keeper': '#96c8ff',
    'maker': '#ff8c32',
    'bridge': '#ffc864',
    'together': '#ffc8ff',
    'cluster': '#ffff64',
    'dim': '#505050',
}

NARRATIVE_SYSTEM_PROMPT = """You are a storyteller who transforms technical ML documentation into engaging narratives.

Style guidelines:
- Write in the style of a fable or parable
- Use a recurring character (like "Mira the Model Maker" or villagers)
- Keep technical accuracy but wrap it in story
- Use poetic language: "whisper-patterns", "the craft of teaching"
- Include the key concepts but make them feel discovered, not lectured
- End with a moral or reflection
- Keep mathematical notation minimal but accurate (use ŷ for predictions, x for features)
- Reference specific examples: ice cream sales, penguin species, diabetes risk

Output format:
- Start with a story title as ## heading
- Use ### for section breaks
- Include a "The moral" section near the end
- End with a link to the original MS Learn content
"""

def fetch_mslearn_content(url: str) -> dict:
    """Fetch and parse content from MS Learn URL."""
    if not HAS_SCRAPING:
        print("Error: Install requests and beautifulsoup4: pip install requests beautifulsoup4")
        return None

    print(f"Fetching: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find main content
    main = soup.find('main') or soup.find('article') or soup

    # Extract title
    title = soup.find('h1')
    title_text = title.get_text().strip() if title else "Untitled"

    # Extract text content
    paragraphs = main.find_all(['p', 'li', 'h2', 'h3'])
    content = []
    for p in paragraphs:
        text = p.get_text().strip()
        if text and len(text) > 20:
            content.append(text)

    return {
        'title': title_text,
        'url': url,
        'content': '\n\n'.join(content)
    }

def transform_to_narrative(content: dict, custom_title: str = None) -> str:
    """Transform technical content to narrative using Claude."""
    if not HAS_ANTHROPIC:
        print("Error: Install anthropic: pip install anthropic")
        return None

    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set")
        return None

    client = anthropic.Anthropic(api_key=api_key)

    title = custom_title or content['title']

    prompt = f"""Transform this Microsoft Learn content about machine learning into a narrative story.

Title to use: {title}
Original URL: {content['url']}

Technical content:
{content['content'][:8000]}

Write a story in the Verse-StoryPath style. Make it engaging, poetic, but technically accurate."""

    print("Transforming to narrative...")
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        system=NARRATIVE_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )

    narrative = response.content[0].text

    # Add source link if not present
    if content['url'] not in narrative:
        narrative += f"\n\n---\n\nFor more detail, see the official Microsoft Learn lesson:\n{content['url']}\n"

    return narrative

def generate_midjourney_prompt(title: str, content: str) -> str:
    """Generate a Midjourney prompt for the lesson."""
    # Extract key themes
    themes = []
    if 'regression' in content.lower():
        themes.append('scattered points becoming a line')
    if 'classification' in content.lower():
        themes.append('sorting, categorizing')
    if 'cluster' in content.lower():
        themes.append('groups forming naturally')
    if 'supervised' in content.lower():
        themes.append('teacher and student')
    if 'model' in content.lower():
        themes.append('mechanical contraption, gears')

    theme_str = ', '.join(themes) if themes else 'machine learning, patterns'

    prompt = f"{title}, {theme_str}, industrial collage art style, weathered wall texture, muted colors with red and orange accents, Bauhaus influence --ar 1:1 --style raw"

    return prompt

def create_lesson(lesson_num: int, title: str, content: str):
    """Create a new lesson markdown file."""
    filename = f"{lesson_num:02d}-{title.lower().replace(' ', '-').replace(':', '')}.md"
    filepath = LESSONS_DIR / filename

    with open(filepath, 'w') as f:
        f.write(content)

    print(f"Created: {filepath}")
    return filepath

def add_image_to_lesson(lesson_num: int, image_path: str):
    """Add an image to a lesson."""
    # Find the lesson file
    pattern = f"{lesson_num:02d}-*.md"
    matches = list(LESSONS_DIR.glob(pattern))

    if not matches:
        print(f"Error: No lesson found matching {pattern}")
        return None

    lesson_file = matches[0]

    # Copy image
    image_name = f"{lesson_num:02d}-{lesson_file.stem.split('-', 1)[1]}.png"
    dest_path = IMAGES_DIR / image_name

    shutil.copy(image_path, dest_path)
    print(f"Copied image to: {dest_path}")

    # Update markdown
    with open(lesson_file, 'r') as f:
        content = f.read()

    # Find first heading and add image after it
    lines = content.split('\n')
    new_lines = []
    image_added = False

    for i, line in enumerate(lines):
        new_lines.append(line)
        if not image_added and line.startswith('## '):
            # Add image after heading
            new_lines.append('')
            new_lines.append(f'![{line[3:].strip()}](../images/{image_name})')
            image_added = True

    with open(lesson_file, 'w') as f:
        f.write('\n'.join(new_lines))

    print(f"Updated: {lesson_file}")
    return dest_path

def generate_embermovie(lesson_num: int):
    """Generate an EmberMovie HTML for a lesson."""
    # Find the lesson file
    pattern = f"{lesson_num:02d}-*.md"
    matches = list(LESSONS_DIR.glob(pattern))

    if not matches:
        print(f"Error: No lesson found matching {pattern}")
        return None

    lesson_file = matches[0]

    with open(lesson_file, 'r') as f:
        content = f.read()

    # Extract title
    title_match = re.search(r'^## (.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else "Untitled"

    # Extract sections for scenes
    sections = re.split(r'^### ', content, flags=re.MULTILINE)

    # Generate HTML (simplified - would use template in production)
    html_file = lesson_file.with_suffix('.html')

    # For now, just note that we'd generate here
    print(f"EmberMovie generation would create: {html_file}")
    print("(Full template system to be implemented)")

    return html_file

def publish(lesson_num: int = None, message: str = None):
    """Commit and push changes to GitHub."""
    os.chdir(REPO_ROOT)

    # Stage changes
    subprocess.run(['git', 'add', 'lessons/', 'images/'], check=True)

    # Create commit message
    if not message:
        if lesson_num:
            message = f"Add/update lesson {lesson_num:02d}"
        else:
            message = "Update lessons"

    full_message = f"""{message}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"""

    # Commit
    result = subprocess.run(['git', 'commit', '-m', full_message], capture_output=True, text=True)
    if result.returncode != 0:
        if 'nothing to commit' in result.stdout + result.stderr:
            print("Nothing to commit")
            return
        print(f"Commit error: {result.stderr}")
        return

    # Push
    subprocess.run(['git', 'push'], check=True)
    print("Published to GitHub!")

def main():
    parser = argparse.ArgumentParser(description='Verse-StoryPath Pipeline')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new lesson from MS Learn URL')
    create_parser.add_argument('--url', required=True, help='MS Learn URL')
    create_parser.add_argument('--lesson', type=int, required=True, help='Lesson number')
    create_parser.add_argument('--title', required=True, help='Lesson title')

    # Add image command
    image_parser = subparsers.add_parser('add-image', help='Add image to a lesson')
    image_parser.add_argument('--lesson', type=int, required=True, help='Lesson number')
    image_parser.add_argument('--image', required=True, help='Path to image')

    # Generate movie command
    movie_parser = subparsers.add_parser('generate-movie', help='Generate EmberMovie HTML')
    movie_parser.add_argument('--lesson', type=int, required=True, help='Lesson number')

    # Publish command
    publish_parser = subparsers.add_parser('publish', help='Commit and push to GitHub')
    publish_parser.add_argument('--lesson', type=int, help='Lesson number (optional)')
    publish_parser.add_argument('--message', help='Custom commit message')

    # Full pipeline command
    full_parser = subparsers.add_parser('full', help='Run full pipeline')
    full_parser.add_argument('--url', required=True, help='MS Learn URL')
    full_parser.add_argument('--lesson', type=int, required=True, help='Lesson number')
    full_parser.add_argument('--title', required=True, help='Lesson title')
    full_parser.add_argument('--image', help='Path to image (optional)')

    # Prompt command - generate Midjourney prompt
    prompt_parser = subparsers.add_parser('prompt', help='Generate Midjourney prompt')
    prompt_parser.add_argument('--lesson', type=int, required=True, help='Lesson number')

    args = parser.parse_args()

    if args.command == 'create':
        content = fetch_mslearn_content(args.url)
        if content:
            narrative = transform_to_narrative(content, args.title)
            if narrative:
                create_lesson(args.lesson, args.title, narrative)
                # Also output Midjourney prompt
                mj_prompt = generate_midjourney_prompt(args.title, narrative)
                print(f"\nMidjourney prompt:\n{mj_prompt}")

    elif args.command == 'add-image':
        add_image_to_lesson(args.lesson, args.image)

    elif args.command == 'generate-movie':
        generate_embermovie(args.lesson)

    elif args.command == 'publish':
        publish(args.lesson, args.message)

    elif args.command == 'full':
        # Full pipeline
        content = fetch_mslearn_content(args.url)
        if content:
            narrative = transform_to_narrative(content, args.title)
            if narrative:
                create_lesson(args.lesson, args.title, narrative)

                if args.image:
                    add_image_to_lesson(args.lesson, args.image)

                generate_embermovie(args.lesson)

                # Output Midjourney prompt if no image provided
                if not args.image:
                    mj_prompt = generate_midjourney_prompt(args.title, narrative)
                    print(f"\nMidjourney prompt:\n{mj_prompt}")

                publish(args.lesson, f"Add lesson {args.lesson:02d}: {args.title}")

    elif args.command == 'prompt':
        pattern = f"{args.lesson:02d}-*.md"
        matches = list(LESSONS_DIR.glob(pattern))
        if matches:
            with open(matches[0], 'r') as f:
                content = f.read()
            title_match = re.search(r'^## (.+)$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else "ML Lesson"
            prompt = generate_midjourney_prompt(title, content)
            print(f"Midjourney prompt:\n{prompt}")
        else:
            print(f"No lesson found matching {pattern}")

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
