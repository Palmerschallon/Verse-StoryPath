# Verse-StoryPath Tools

Pipeline for creating narrative ML lessons with EmberMovie animations.

## Setup

```bash
pip install anthropic requests beautifulsoup4
export ANTHROPIC_API_KEY="your-key"
```

## Usage

### Create a new lesson from MS Learn

```bash
./verse create --url "https://learn.microsoft.com/..." --lesson 5 --title "The Tale of Classification"
```

This will:
1. Fetch content from MS Learn
2. Transform it to narrative using Claude
3. Create the markdown file
4. Output a Midjourney prompt for the image

### Add an image to a lesson

```bash
./verse add-image --lesson 5 --image ~/Downloads/image.png
```

### Generate EmberMovie HTML

```bash
./verse generate-movie --lesson 5
```

### Publish to GitHub

```bash
./verse publish --lesson 5
```

### Full pipeline

```bash
./verse full --url "URL" --lesson 5 --title "Title" --image ~/Downloads/image.png
```

### Generate Midjourney prompt for existing lesson

```bash
./verse prompt --lesson 3
```

## Workflow

1. Find MS Learn lesson URL
2. Run `./verse create --url URL --lesson N --title "Title"`
3. Copy the Midjourney prompt and generate image
4. Download image to ~/Downloads
5. Run `./verse add-image --lesson N --image ~/Downloads/latest.png`
6. Run `./verse publish --lesson N`

## File Structure

```
Verse-StoryPath/
├── lessons/
│   ├── 01-introduction-bridge-builders.md
│   ├── 01-introduction-bridge-builders.html  # EmberMovie
│   ├── 02-machine-learning-models.md
│   └── ...
├── images/
│   ├── 01-bridge-hero.png
│   ├── 02-model-maker.png
│   └── ...
└── tools/
    ├── verse          # Shell wrapper
    ├── verse.py       # Main pipeline
    └── README.md
```
