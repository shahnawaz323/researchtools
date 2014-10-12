#!/bin/bash

# Kurt Schwehr - Sept 2011
# BSD License
# Warning: This will not work for a Mac or Windows desktop

while [ true ]
do
    echo $(date +%H%M%S).png 
    # Use ImageMagick / GraphicsMagick to grab the X11 screen.
    import -window root $(date +%H%M%S).png 
    sleep 5
done
