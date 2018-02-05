#!/usr/bin/env python

import argparse
import os
import fileinput
import shutil
from datetime import datetime
import string
import sys


""" Takes in one argument --name, creates directory and the following subdirectories
# images, src, notes, and adds a template xaringan Rpresentation file.
"""

# Before we begin, are we using python 3.6 or greater?
try:
    assert sys.version_info >= (3, 6)
except AssertionError:
    sys.exit("Error: Python version out of date. Require 3.6 or higher.")

# Get arguments
parser = argparse.ArgumentParser(description="Create presentation folder")
parser.add_argument("--name", required=True, type=str,
                    help="name of the presentation")
parser.add_argument("--author", required=True, type=str,
                    help="author of presentation")
args = parser.parse_args()

# Check args.
# Check name does not contain spaces or any other special characters
allowed_chars=string.ascii_letters + string.digits + '_-'
if not args.name.translate(allowed_chars) == args.name:
    illegal_chars = set(args.name).difference(args.name.translate(allowed_chars))
    illegal_chars = [f"\'{character}\'" for character in illegal_chars]
    sys.exit(f"Error, illegal characters in name argument.\n" +
             f"Please enusre this consists of letters and numbers only.\n" +
             f"You have entered the following characters which are forbidden:\n {' '.join(illegal_chars)}")
# Get path of this script.
script_dir = os.path.dirname(os.path.realpath(__file__))

os.chdir(script_dir)

# Create presentation directory
presentation_dir = os.path.join(script_dir, args.name)
if not os.path.isdir(presentation_dir):
    os.mkdir(presentation_dir)

# Pull xaringan template from Template folder
shutil.copy(os.path.join("Template", "template_xaringan.Rmd"), os.path.join(presentation_dir, args.name+".Rmd"))
# We will also need to copy across the generated libs folder
shutil.copytree(os.path.join("Template", "libs"), os.path.join(presentation_dir, "libs"))
# Rename example.css
shutil.move(os.path.join(presentation_dir, "libs", "remark-css-0.0.1", "example.css"),
            os.path.join(presentation_dir, "libs", "remark-css-0.0.1", args.name + ".css"))

# Create presentation directory subfolders
subfolders = ["images", "src", "docs", "references"]

for subfolder in subfolders:
    if not os.path.isdir(os.path.join(presentation_dir, subfolder)):
        os.mkdir(os.path.join(presentation_dir, subfolder))

# Manipulate Xaringan Rmd file to automatically place in author and presentation name.
with fileinput.FileInput(os.path.join(presentation_dir, args.name+".Rmd"), inplace=True) as file:
    for line in file:
        line = line.replace("%name%", args.name)
        line = line.replace("%author%", args.author)
        line = line.replace("%date%", datetime.today().strftime('%a %d %b %Y'))
        print(line)
