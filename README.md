# Image Titler

[![Join the chat at https://gitter.im/TheRenegadeCoder/image-titler](https://badges.gitter.im/TheRenegadeCoder/image-titler.svg)](https://gitter.im/TheRenegadeCoder/image-titler?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Adds a title to an image using The Renegade Coder Featured Image style. The style can be
defined as the following:

> Titles are split in half by the closest space and displayed using two solid red bars
> with a white text overlay on the upper right portion of the image.

For example:

![Hello World in Pascal](https://i0.wp.com/therenegadecoder.com/wp-content/uploads/2018/04/hello-world-in-pascal-featured-image.jpeg?resize=1024%2C640&ssl=1)

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
```
