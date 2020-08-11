# Image Titler

[![Discord](https://img.shields.io/discord/612072397545275424)](https://discord.gg/Jhmtj7Z)  


The Image Titler is a tool which provides options for generating thumbnails for various social media platforms.
Currently, the tool has a predefined style which looks roughly like the following image:

![23 Tech Topics to Tackle](https://raw.githubusercontent.com/TheRenegadeCoder/image-titler/master/samples/v1.8.0/23-tech-topics-to-tackle-featured-image-v1-8-0.JPEG)

To see more examples, check out our [list of samples](https://github.com/TheRenegadeCoder/image-titler/tree/master/samples).

## How to Run

The following code snippet demonstrates a few ways you might use the script:

```shell
pip install image-titler # Installs the script

image-titler # Runs as default
image-titler --title "Hello, World!"  # Adds a custom title
image-titler --output_path "path/to/output"  # Sets the output path
image-titler --path "path/to/image"  # Sets the image path
image-titler --tier "free"  # Sets the membership tier which changes the rectangle borders
image-titler --logo_path "path/to/logo"  # Adds a 145x145 logo to the lower left corner of the image
image-titler --batch  # Runs the program in batch mode on a directory
image-titler --font "path/to/font"  # Changes the default title font
image-titler --size YouTube  # Changes the aspect ratio of the output file
```

Alternatively, you can spin up the GUI version of the software as of 2.0.0 as follows:

```shell
image-titler-gui

# Options can be used to preload GUI as of 2.2.0
image-titler-gui --title "Hello, World!"  # Adds a custom title
image-titler-gui --output_path "path/to/output"  # Sets the output path
image-titler-gui --path "path/to/image"  # Sets the image path
image-titler-gui --tier "free"  # Sets the membership tier which changes the rectangle borders
image-titler-gui --logo_path "path/to/logo"  # Adds a 145x145 logo to the lower left corner of the image
image-titler-gui --batch  # Runs the program in batch mode on a directory
image-titler-gui --font "path/to/font"  # Changes the default title font
image-titler-gui --size YouTube  # Changes the aspect ratio of the output file
```

## Default Behavior

Currently, the image-titler script makes a few assumptions about the images it 
processes automatically: 

- This tool scrapes file names for image titles. To do this, it assumes 
file names are written in kebab-case where each word is separated by a hyphen.
Then, words are extracted and title cased before being printed on the image.
- The color of the title bars defaults to The Renegade Coder Red (201, 2, 41, 255).
If you'd like a different color, the script automatically extracts the most dominant
color from logos. At this time, there is no way to customize bar color. 
- Added elements have fixed position. Logos will always appear in the bottom left.
Titles will always appear in the top right. 

There are likely other default behaviors not documented here. Feel free to experiment
with the tool and share any issues you find. 

## Full List of Options

Here's a description of all the option used in the samples above.

| Option | Domain | Description |
|--------|--------|-------------|
| --batch, -b | True/False | Turns on batch processing |
| --font, -f | Any valid font file | Overrides the default title font |
| --logo_path, -l | Any valid image file | Loads a logo onto the input image |
| --output_path, -o | Any valid directory | Determines where files will be saved (has no effect in GUI) |  
| --path, -p | Any valid file or directory | Loads the input image (or directory when in batch mode) |
| --size, -s | Choose between "Twitter", "WordPress", and "YouTube" | Sets the aspect ratio of the output image |
| --tier, -r | Choose between "free" (silver) or "premium" (gold) | Adds a border color to the title |
| --title, -t | Any string | Overrides the automatic title feature |
