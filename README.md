# Image Titler

[![Join the chat at https://gitter.im/TheRenegadeCoder/image-titler](https://badges.gitter.im/TheRenegadeCoder/image-titler.svg)](https://gitter.im/TheRenegadeCoder/image-titler?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Adds a title to an image using The Renegade Coder Featured Image style. The style can be
defined as the following:

> Titles are split in half by the closest space and displayed using two solid red bars
> with a white text overlay on the upper right portion of the image. In addition, logos
> can be added which will affect the bar color. 

For example:

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
```

Alternatively, you can spin up the GUI version of the software as of 2.0.0 as follows:

```shell
image-titler-gui
```

At this time, the GUI does not feature the same command line interface. 

## Default Behavior

Currently, the image-titler script makes a few assumptions about the images it 
processes automatically: 

- The size of an image is assumed to be 1920x960. Otherwise, this tool 
will automatically crop the image to size. 
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
