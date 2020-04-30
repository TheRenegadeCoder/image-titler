# Sample Image Titles

In this archive, I'll share a series of samples that are output by this program. That said,
here's a quick video overview:

![Image Titler 2.0.0 GIF](v2.0.0/image-titler.gif)

## Default Behavior

The following image is an example of the default behavior of this program as of v1.8.0:

![23 Tech Topics to Tackle](v2.0.0/23-tech-topics-to-tackle-featured-image-v2-0-0.JPEG)

Here's the command that would generate this image:

```shell script
image-titler
```

## Logo Behavior

The following image is an example of the behavior when the script is provided a logo as of 1.8.0:

![3 Ways to Check If a List is Empty in Python](v2.0.0/3-ways-to-check-if-a-list-is-empty-in-python-featured-image-v2-0-0.JPEG)

When using a logo, title background color is generated automatically. Here's another example:

![Hello World in MATLAB](v2.0.0/hello-world-in-matlab-featured-image-v2-0-0.JPEG)

Here's the command that would generate these images:

```shell script
image-titler -l "path/to/logo"
```

# Tier Behavior

The following image is an example of the behavior when the premium subscription tier is applied to the logo as of 1.8.0:

![The Guide to Causing Mass Panic](v2.0.0/the-guide-to-causing-mass-panic-featured-image-v2-0-0.JPEG)

To generate an image like this, use the following command:

```shell script
image-titler -r premium
```

In addition, the script supports a free tier as well:

![Columbus Drivers Are Among the Worst](v2.0.0/columbus-drivers-are-among-the-worst-featured-image-v2-0-0.JPEG)

To generate an image like this, use the following command:

```shell script
image-titler -r free
```