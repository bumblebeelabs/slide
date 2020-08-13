# Slide
Slide is an image viewer for JPEG and PNG files. Unlike typical image viewers, Slide
does not display window dressings such as scrollbars, window frames, or borders
(black or white or any other areas not found in the original image file).

This unusual format allows sharing of pictures over teleconferencing applications
like [Zoom](https://zoom.us/) without the scrollbars, window frames, or borders
that detract from or spoils the participants' view of the image, in particular
window dressings that make the image smaller and hard to see.

To further minimize disruptions to the participant's experience, keyboard keys
are available to advance to the next image in the directory.

Slide can be used in slide mode. Images are shown briefly, one after another, and
looping back to the first. This avoids host fatigue.
# Prerequisites

```
dnf install python3-pyside2
```

# Installing
A script is available for installing on GNOME desktops:

```
./setup.sh
```

After installing on GNOME desktops, use the ```Files``` app to associate ```png```, ```jpg``` and ```jpeg``` file extensions with ```Display Slides```.

# Usage
Double click an image file in ```File``` to display the image.

These are the keyboard controls:

* <kbd>→</kbd> - next image
* <kbd>←</kbd> - previous image
* <kbd>SPACE</kbd> - toggle image / slides mode
* <kbd>?</kbd> - toggle file name display
