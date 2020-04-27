# Image Titler

[![Join the chat at https://gitter.im/TheRenegadeCoder/image-titler](https://badges.gitter.im/TheRenegadeCoder/image-titler.svg)](https://gitter.im/TheRenegadeCoder/image-titler?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Adds a title to an image using The Renegade Coder Featured Image style. The style can be
defined as the following:

> Titles are split in half by the closest space and displayed using two solid red bars
> with a white text overlay on the upper right portion of the image.

For example:

![23 Tech Topics to Tackle](https://raw.githubusercontent.com/TheRenegadeCoder/image-titler/master/samples/23-tech-topics-to-tackle-featured-image-v1-8-0.JPEG)

To see more examples, check out our [list of samples](https://github.com/TheRenegadeCoder/image-titler/tree/master/samples).

## How to Run

The following code snippet demonstrates a few ways you might use the script:

```shell
pip install image-titler # Installs the script

image_titler # Runs as default
image_titler --title "Hello, World!"  # Adds a custom title
image_titler --output_path "path/to/output"  # Sets the output path
image_titler --path "path/to/image"  # Sets the image path
image_titler --tier "free"  # Sets the membership tier which changes the rectangle borders
image_titler --logo_path "path/to/logo"  # Adds a 145x145 logo to the lower left corner of the image
image_titler --batch # Runs the program in batch mode on a directory
```
