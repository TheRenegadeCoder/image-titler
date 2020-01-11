import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="image-titler",
    version="1.5.1",
    author="The Renegade Coder",
    author_email="jeremy.grifski@therenegadecoder.com",
    description="Adds a title to an image using The Renegade Coder Featured Image style",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheRenegadeCoder/image-titler",
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            'image_titler = image_titler.trc_image_titler:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'titlecase',
        'pillow>=6.0.0'
    ],
)
