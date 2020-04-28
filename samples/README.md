# Sample Image Titles

In this archive, I'll share a series of samples that are output by this program.

## Default Behavior

The following image is an example of the default behavior of this program as of v1.8.0:

![3 Ways to map Two Lists to a Dict in Python](v1.8.0/3-ways-to-map-two-lists-to-a-dict-in-python-featured-image-v1-8-0.JPEG)

Here's the command that would generate this image:

```shell script
image_titler
```

## Logo Behavior

The following image is an example of the behavior when the script is provided a logo as of 1.8.0:

![23 Tech Topics to Tackle](v1.8.0/23-tech-topics-to-tackle-featured-image-v1-8-0.JPEG)

When using a logo, title background color is generated automatically. Here's another example:

![Hello World in MATLAB](v1.8.0/hello-world-in-matlab-featured-image-v1-8-0.JPEG)

Here's the command that would generate these images:

```shell script
image_titler -l "path/to/logo"
```

# Tier Behavior

The following image is an example of the behavior when the premium subscription tier is applied to the logo as of 1.8.0:

![Is the Work Finally Paying Off?](v1.8.0/is-the-work-finally-paying-off-featured-image-v1-8-0.JPEG)

To generate an image like this, use the following command:

```shell script
image_titler -r premium
```

In addition, the script supports a free tier as well:

![Technical Writers in Need](v1.8.0/technical-writers-in-need-featured-image-v1-8-0.JPEG)

To generate an image like this, use the following command:

```shell script
image_titler -r free
```