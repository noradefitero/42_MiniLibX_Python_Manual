---
title: MiniLibX Python Manual
abstract: >
  This documentation is a PORT of the ORIGINAL MiniLibX docs.

  It describes the Python package that provides access to the MiniLibX
  graphics library. It allows creating windows, drawing pixels, handling
  images, and capturing keyboard and mouse input through a thin wrapper over
  the original C API, keeping function names and behavior as close as possible
  to the native MiniLibX library.
author: "Nora de Fitero Teijeira (noradefitero)"
titlepage-logo: "media/42_MiniLibX_Python_Manual.jpg"
logo-width: 300px
acknowledgements: >
  The original MiniLibX documentation was created by Olivier Crouzet under the
  MIT license. This is a derivative work based on his work, created on a
  non-profit basis with the aim of sharing knowledge among the 42 student
  community.

  This derivative work is published under the MIT license by Nora de Fitero
  Teijeira. Copies of the licenses can be found in the GitHub repository for
  this documentation.
---

<!-- markdownlint-disable MD013 MD024 -->

## Got any suggestions?

If you find any errors or have any new ideas for improving this manual, feel
free to open an Issue or Pull Request, or contact me at my email address:
<nora@defitero.com>

## Introduction

The MinilibX or MLX is a library written in C (we’ll come back to that) that provides a very simple API to the graphic capabilities. It's designed to be easy enough for early stage coders that could not immediately use standard graphical libraries and windowing systems.

The set of features is limited, on purpose, and is not meant to be extended. The learners have to build more advanced features, hence developing their own coding skills.

It provides:

- Window creation and management
- Pixel-level drawing
- Image manipulation for faster rendering
- Keyboard and mouse input handling
- PNG and XPM image loading

### How a graphics server works

This library interacts with the underlying graphics system of your operating
system. Before diving into usage, it's helpful to understand how graphics
servers manage windows and handle user input.

#### Unix/Linux: Historical X-Window concept

The X Window System, often called X11, is the software layer that draws text and graphics on the screen. X does not decide how applications look: that is the job of each X client, of a window manager such as Window Maker or Tab Window Manager, or of a complete desktop environment like KDE, GNOME or Xfce.

X is cross-platform: Linux, the BSDs, Solaris and other Unix-like systems all support it, and implementations exist for Apple’s macOS and Microsoft Windows as well.

It is based on two main parts:

- On one side, your software wants to draw something on the screen and/or get
  keyboard & mouse entries.

- On the other side, the X-Server manages the screen, keyboard and mouse (It is
  often referred to as a \"display\").

A network connection must be established between these two entities to send
drawing orders (from the software to the X-Server), and keyboard/mouse events
(from the X-Server to the software).

Nowadays, most of the time, both run on the same computer.

![The X Window System: applications are X clients, while the X server owns the display and sends input events back to the clients.](media/diagram-x11.svg)

#### Unix/Linux: Wayland, the modern graphical approach

Modern computers come with a powerful GPU that is directly accessed by
applications. Along GPU libraries like Vulkan or OpenGL, the Wayland protocol
ensures communication with the compositor program that manages the various
windows on screen and the user input events. For your own application:

- The Vulkan or OpenGL library allows you to directly draw any content into your
  window.
- The Wayland compositor handles the place of your window on screen and sends you
  back the keyboard and mouse inputs from the user.

Unfortunately, this gain of graphical power through GPU access removes the
networking aspects that exist with X-Window. It is not possible for a program to
access a remote GPU and show its window on a remote display. But current
software architectures are more likely based on a local display application that
gets data in JSON through a web API.

![Wayland: the application draws directly via Vulkan/OpenGL and talks to the compositor for input and window placement.](media/diagram-wayland.svg)

#### MacOS: Window server and GPU

Your software interacts directly with the Window server that handles the cohabitation on the screen with other software and the event system, and interacts with the GPU to handle all drawing commands.

## Getting started

### Requirements

These lists cover building from source. MiniLibX is supported on Linux (XCB backend by default, Wayland optional) and macOS (Intel and Apple Silicon). Windows is not supported (there is no Win32 backend), and WSL is not officially documented (it may work under WSLg, but without guarantees). The examples in this manual use Python type hints such as `X | None`, which require Python 3.10 or newer; the library itself does not declare a minimum version.

#### Homebrew (macOS)

The macOS build uses the AppKit backend, which needs a Vulkan implementation on
top of Metal.

- Xcode command-line tools (`xcode-select --install`)

```bash
brew install vulkan-loader vulkan-tools molten-vk
```

MoltenVK provides the `libMoltenVK.dylib` driver the AppKit backend links
against; `configure.sh` reports it as missing, and the build fails without it.

#### Arch Linux

XCB backend (the default):

```bash
sudo pacman -S libxcb xcb-util-keysyms zlib libbsd vulkan-icd-loader vulkan-headers vulkan-tools shaderc
```

Wayland backend (optional):

```bash
sudo pacman -S wayland wayland-protocols libxkbcommon
```

shaderc is only needed to recompile the shaders; the precompiled ones are shipped with the library.

#### Debian/Ubuntu

XCB backend (the default):

```bash
sudo apt install libxcb1-dev libxcb-keysyms1-dev libvulkan-dev zlib1g-dev libbsd-dev glslc
```

Wayland backend (optional):

```bash
sudo apt install libwayland-dev libxkbcommon-dev wayland-protocols libwayland-bin
```

These are the development packages (the ones needed to compile). The linker
flags they provide are `-lxcb -lxcb-keysyms -lvulkan -lz -lbsd`.

### Build source code (Recommended way)

These steps must be performed on every machine/architecture where the library will be run.

#### Clone the repository

```bash
git clone https://github.com/42school/mlx_CLXV.git
```

#### Run compiling scripts

Execute the configuration script provided:

```bash
./configure.sh
```

Then compile MiniLibX:

```bash
make
```

A Python package named after the library version should appear in the root of the repository (currently `mlx-2.4-py3-none-any.whl`).

### Get the compiled package from intra (not recommended)

On the 42 intranet, in the Python projects that use MLX (a_maze_ing, etc.), you’ll find a folder containing .whl files.

![The mlx folder on the 42 intranet listing the precompiled .whl packages, one per platform and architecture.](media/intra-mlx-folder-preview.jpg)

These can be used as a fallback if you’ve had trouble compiling MinilibX, but it’s not recommended to use them as your primary method. Since they were compiled on other computers, in different environments, or on different architectures, they may cause problems on your PC or any other machine.

> [!NOTE]
> In case you get an error when installing the distributed packages, try changing
> the name to **mlx-2.4-py3-none-any.whl**.

### Install the wheel

Create a virtual environment with your preferred manager and open it:

- For bash/Zsh:

```bash
python -m venv .venv
source .venv/bin/activate
```

- For fish:

```bash
python -m venv .venv
source .venv/bin/activate.fish
```

And install the package:

```bash
pip install mlx-2.4-py3-none-any.whl
```

> [!TIP]
> Do you find virtual environments confusing? Try uv, a version and project manager written in Rust. More info in their documentation: [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

![Chart with benchmark results. From uv's docs](media/uv-benchmark.svg)

### Example of use

This small Python script displays a small black window with text. It will also
print the screen dimensions to stdout and listen for user clicks.

We will explain the functions used in this example later.

```python
from mlx import Mlx


def mymouse(button, x, y, mystuff):
    print(f"Got mouse event! button {button} at {x},{y}.")


def mykey(keynum, mystuff):
    print(f"Got key {keynum}, and got my stuff back:")
    print(mystuff)
    if keynum == 32:
        m.mlx_mouse_hook(win_ptr, None, None)


m = Mlx()
mlx_ptr = m.mlx_init()
if mlx_ptr is None:
    raise RuntimeError("mlx_init() failed")
win_ptr = m.mlx_new_window(mlx_ptr, 200, 200, "test")
if win_ptr is None:
    raise RuntimeError("mlx_new_window() failed")
m.mlx_clear_window(mlx_ptr, win_ptr)
# 255 = blue, fully opaque (see Color management)
m.mlx_string_put(mlx_ptr, win_ptr, 20, 20, 255, "Hello PyMlx!")
(status, w, h) = m.mlx_get_screen_size(mlx_ptr)
print(f"Got screen size: {w} x {h} .")

stuff = [1, 2]
m.mlx_mouse_hook(win_ptr, mymouse, None)
m.mlx_key_hook(win_ptr, mykey, stuff)

m.mlx_loop(mlx_ptr)
```

Let's walk through it, because this script contains the whole skeleton of
every MiniLibX program:

- `m = Mlx()` creates the Python object that will talk to the C library (see
  [The MLX Wrapper](#the-mlx-wrapper)).
- `mlx_init()` opens the connection to the graphics system. It returns the
  connection identifier `mlx_ptr`, or `None` if it fails.
- `mlx_new_window()` creates the window on that connection. It returns the
  window identifier `win_ptr`, or `None` if it fails.
- `mlx_clear_window()` paints the window black so we start from a clean
  canvas.
- `mlx_string_put()` writes text at (20, 20). The `255` is a color encoded in
  a single integer (see [Color management](#color-management)).
- `mlx_get_screen_size()` returns a `(status, width, height)` tuple; the
  status always comes first.
- `mlx_mouse_hook()` and `mlx_key_hook()` register the functions MiniLibX
  will call when the mouse or the keyboard is used.
- `mlx_loop()` hands control to the event loop (see [Handle
  events](#handle-events)): from now on, your program only runs inside
  callbacks.

> [!IMPORTANT]
> This first example never quits on its own: it runs until you stop it. While
> `mlx_loop()` is running, Python can't catch `Ctrl-C`, so press `Ctrl-\` to
> kill the program. If you'd rather quit gracefully, the next example shows how.

#### A game loop with images and delta time

The previous loop draws with `mlx_clear_window()` and `mlx_string_put()`,
which is fine for a demo. A real game loop follows a different recipe, and
this is the pattern every serious MiniLibX project uses:

1. Create **one** image the size of the window. It is your off-screen
   framebuffer: a canvas you can rewrite freely, without the graphics system
   watching every pixel.
2. Every frame: clear the buffer, draw your scene into it, and stamp it onto
   the window with a single `mlx_put_image_to_window()` call.
3. Measure the time between frames yourself; MiniLibX does not provide a
   delta time.
4. Track which keys are held with a `set` instead of relying on repeated
   events.

```python
import time

from mlx import Mlx

m = Mlx()
mlx_ptr = m.mlx_init()
win_ptr = m.mlx_new_window(mlx_ptr, 640, 480, "Game loop")
img_ptr = m.mlx_new_image(mlx_ptr, 640, 480)
pixels, bpp, size_line, fmt = m.mlx_get_data_addr(img_ptr)

pressed = set()  # keys held right now
last = time.monotonic()


def frame(param):
    global last
    now = time.monotonic()
    dt = now - last  # seconds since last frame
    last = now
    m.mlx_sync(mlx_ptr, m.SYNC_IMAGE_WRITABLE, img_ptr)  # buffer is ours again
    pixels[:] = b"\x00" * len(pixels)  # clear to black
    # ... draw your scene here, using `pressed` and `dt` ...
    m.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)


def on_press(keycode, param):
    pressed.add(keycode)


def on_release(keycode, param):
    pressed.discard(keycode)


m.mlx_hook(win_ptr, 2, 1, on_press, None)  # KeyPress
m.mlx_hook(win_ptr, 3, 2, on_release, None)  # KeyRelease
m.mlx_do_key_autorepeatoff(mlx_ptr)
m.mlx_loop_hook(mlx_ptr, frame, None)
m.mlx_loop(mlx_ptr)
m.mlx_destroy_image(mlx_ptr, img_ptr)
m.mlx_destroy_window(mlx_ptr, win_ptr)
m.mlx_release(mlx_ptr)
```

Don't worry if the event numbers (2, 3) and the sync call look magical yet:
[Handle events](#handle-events) explains the hooks and
[Flush and sync functions](#flush-and-sync-functions) explains
`SYNC_IMAGE_WRITABLE`. The important idea is the recipe above: one buffer,
one blit per frame.

## The MLX Wrapper

The package you install exposes a class called Mlx. But MiniLibX itself is a
C library, and its functions can only be called from C code. The Mlx class is
a thin wrapper: every time you call one of its methods, it converts your
Python arguments into strictly typed C data, calls the real C function, and
converts the result back into Python. You write Python, but the heavy lifting
still happens inside the original C library.

Let's take a closer look at how it works.

### How does the wrapper work?

When an instance of the Mlx class is created, the first thing it does is
construct the path to the C library that ships alongside the package: it is
called libmlx.dylib on macOS and libmlx.so everywhere else.

```python
def __init__(self):
    module_dir = os.path.dirname(os.path.abspath(__file__))
    libname = "libmlx.dylib" if sys.platform == "darwin" else "libmlx.so"
    self.so_file = os.path.join(module_dir, libname)
    # ...
```

- `__file__` is a special Python variable that contains the path to the file
  where this code is executed.

- os.path.dirname extracts the path from `__file__` and uses os.path.join to
  create the path to the library.

It then declares the mlx_func variable, which acts as a bridge between Python
and C. Using the CDLL function from Python's ctypes module, it loads the library
and calls the original functions.

```python
def __init__(self):
    # ...
    self.mlx_func = CDLL(self.so_file)
    # ...
```

For each C function available in the Python wrapper, there is a declaration
within the Mlx class:

```python
def mlx_init(self):
    self.mlx_func.mlx_init.restype = c_void_p
    return self.mlx_func.mlx_init()
```

You can see how it calls mlx_func.mlx_init(). This mlx_init() is already the
original C function. It is necessary to specify the data type returned by the
function with mlx_init.restype, which in this case is c_void_p (equivalent to
void *).

All of this is passed to CDLL, which, using the previously loaded library, will
execute the function and return whatever the function returns.

![The Python wrapper bridges Python method calls to the C MiniLibX library through ctypes, which then talks to the OS graphics subsystem.](media/diagram-python-c-bridge.svg)

### Wrapper conventions

Three things differ from the C API, and they matter in everyday Python code:

- Functions that create resources (`mlx_init()`, `mlx_new_window()`,
  `mlx_new_image()`) return `None` when they fail, instead of raising an
  exception. Always check the result.
- C functions that hand back extra values through pointer arguments become
  Python methods that return a tuple, and the status comes first:

```python
status, width, height = m.mlx_get_screen_size(mlx_ptr)
status, x, y = m.mlx_mouse_get_pos(win_ptr)
img, width, height = m.mlx_png_file_to_image(mlx_ptr, "sprite.png")
```

- `mlx_get_data_addr()` returns a writable `memoryview`, so you can modify
  image pixels with plain Python slice assignment.

> [!IMPORTANT]
> Forgetting the leading status when unpacking these tuples is the most common
> beginner mistake: `width, height = m.mlx_get_screen_size(mlx_ptr)` fails at
> runtime. The status is always the first element.

## Initialization and cleanup

Every program starts here: a connection to the graphics system, and a polite
goodbye when you are done. Think of _mlx_ptr_ as the phone line to the display
server: every other function needs it to know where to send its orders.

### Synopsis

```python
def mlx_init() -> int | None: # void *

def mlx_release(mlx_ptr: int | None) -> int:
```

### Description

First of all, you need to initialize the connection between your software and
the graphic and user sub-systems. Once this completed, you'll be able to use
other MiniLibX functions to send and receive the messages from the display, like
"I want to draw a yellow pixel in this window" or "did the user hit a key?".

The mlx_init function will create this connection. No parameters are needed, and
it will return an `int` (void *), used for further calls to the library
routines.

The mlx_release function can be used at the end of the program to
disconnect from the graphic system and release resources.

If **mlx_init()** fails to set up the connection to the display, it will return
`None`.

### Return values

If **mlx_init**() set up the connection to the display correctly, it will return
an **int as a pointer**; otherwise, it returns **None**.

_In one sentence:_ `mlx_init()` opens the line to the graphics system,
`mlx_release()` hangs up, and every other function borrows that line while
it is open.

## Managing windows

Once the connection is open, you need somewhere to draw. Windows are your
canvases on screen: MiniLibX can manage several of them at once, each with its
own size, title and hooks.

### Synopsis

```python
def mlx_new_window(mlx_ptr: int | None, width: int, height: int, title: str) -> int | None: # void *

def mlx_clear_window(mlx_ptr: int | None, win_ptr: int | None) -> int:

def mlx_destroy_window(mlx_ptr: int | None, win_ptr: int | None) -> int:
```

### Description

The **mlx_new_window**() function creates a new window on the screen, using the
_width_ and _height_ parameters to determine its size, and _title_ as the text
that should be displayed in the window's title bar.

The _mlx_ptr_ parameter is the connection identifier returned by **mlx_init**()
(see the **mlx** man page). **mlx_new_window**() returns a _void \*_ window
identifier that can be used by other MiniLibX calls.

Note that the MiniLibX can handle an arbitrary number of separate windows.

**mlx_clear_window**() and **mlx_destroy_window**() respectively clear (in
black) and destroy the given window. They both have the same parameters:
_mlx_ptr_ is the screen connection identifier, and _win_ptr_ is a window
identifier.

### Return values

If **mlx_new_window()** fails to create a new window (whatever the reason), it
will return None, otherwise a non-null pointer (integer) is returned as a window
identifier.

**mlx_clear_window**() and **mlx_destroy_window**() return 0.

_In one sentence:_ windows are your canvases on screen: create them, draw on
them, and destroy them only after the loop has ended.

## Drawing inside windows

The simplest way to put something on screen is to color a single pixel.
`mlx_pixel_put()` and `mlx_string_put()` draw directly into a window: easy to
use and perfect for learning, but slow when you need thousands of pixels. Use
them to experiment and debug; use [images](#manipulating-images) for real
rendering.

### Synopsis

```python
def mlx_pixel_put(mlx_ptr: int | None, win_ptr: int | None, x: int, y: int, color: int) -> int:

def mlx_string_put(mlx_ptr: int | None, win_ptr: int | None, x: int, y: int, color: int, string: str) -> int:
```

### Description

The **mlx_pixel_put**() function draws a defined pixel in the window _win_ptr_
using the ( _x_ , _y_ ) coordinates, and the specified _color_.

![Window coordinates: (0,0) is the top-left corner, x grows right and y grows down.](media/diagram-coordinates.svg)

Parameters for **mlx_string_put**() have the same meaning. Instead of a simple
pixel, the specified _string_ will be displayed at ( _x_ , _y_ ).

Both functions will discard any display outside the window. This makes
**mlx_pixel_put** slow. Consider using images instead.

### Color management

The _color_ parameter has an unsigned integer type. The displayed colour needs
to be encoded in this integer, following a defined scheme. All displayable
colours can be split in 3 basic colours: red, green and blue. Three associated
values, in the 0-255 range, represent how much of each colour is mixed up to
create the original colour. The fourth byte represents transparency, where 0 is fully transparent and 255
opaque.

These four values must be set inside the unsigned integer to display the right
colour. The bytes of this integer are filled in 32-bit color packing (little-endian), as shown in the picture below:

![A color is packed into a 32-bit integer as four bytes: blue, green, red and alpha.](media/diagram-color-bytes.svg)

While filling the integer, make sure you avoid endian problems.

Example: the \"blue\" byte will be the least significant byte inside the integer
on a little endian machine.

## Manipulating images

### Synopsis

```python
def mlx_new_image(mlx_ptr: int | None, width: int, height: int) -> int | None: # void *

def mlx_get_data_addr(img_ptr: int | None) -> Tuple[memoryview, int, int, int]: # (pixels, bits_per_pixel, size_line, format)

def mlx_put_image_to_window(mlx_ptr: int | None, win_ptr: int | None, img_ptr: int | None, x: int, y: int) -> int:

def mlx_xpm_file_to_image(mlx_ptr: int | None, filename: str) -> Tuple[Optional[int], int, int]: # (image: void *, width, height)

def mlx_png_file_to_image(mlx_ptr: int | None, filename: str) -> Tuple[Optional[int], int, int]: # (image: void *, width, height)

    def mlx_destroy_image(mlx_ptr: int | None, img_ptr: int | None) -> int:
```

### Description

**mlx_new_image**() creates a new image in memory. It returns an _int pointer_
needed to manipulate this image later. It only needs the size of the image to be
created, using the _width_ and _height_ parameters, and the _mlx_ptr_ connection
identifier.

The user can draw inside the image (see below), and can dump the image inside a
specified window at any time to display it on the screen. This is done using
**mlx_put_image_to_window**(). Three identifiers are needed here, for the
connection to the display, the window to use, and the image (respectively
_mlx_ptr_ , _win_ptr_ and _img_ptr_ ). The ( _x_, _y_ ) coordinates define where
the image should be placed in the window.

**mlx_get_data_addr**() returns information about the created image, allowing a
user to modify it later. The _img_ptr_ parameter specifies the image to use. It
returns the tuple ( _pixels_ , _bits_per_pixel_ , _size_line_ , _format_ ).
_pixels_ is a writable memoryview over the image buffer (bytes: _height_ \*
_size_line_ ). _bits_per_pixel_ is the number of bits needed to represent a
pixel colour (also called the depth of the image). _size_line_ is the number of
bytes used to store one line of the image in memory (the stride); this
information is needed to move from one line to another in the image. _format_
tells you how each pixel colour in the image is structured.

Currently only 2 values are defined:

- 0 means format B8G8R8A8
- 1 means format A8R8G8B8

The offset of a pixel is computed as
`offset = y * size_line + x * (bits_per_pixel // 8)`; the following 4 bytes are
the colour of that pixel.

**mlx_destroy_image** destroys the given image ( _img_ptr_ ).

### Storing colours inside images

Depending on the graphic system, the number of bits used to store a pixel colour
used to be different from one hardware to another. Today, the way the user
usually represents a colour, in the ARGB mode, almost always matches the
hardware capabilities on modern computers.

Keep in mind that packing the 4-byte ARGB into an unsigned int depends on the
local computer's endian. Adjust your code accordingly.

You can paint a pixel by writing directly into the writable memoryview returned
by **mlx_get_data_addr**():

```python
pixels, bpp, size_line, fmt = m.mlx_get_data_addr(img_ptr)
x, y = 10, 20
offset = y * size_line + x * (bpp // 8)
# format 0 (B8G8R8A8): blue, green, red, alpha
pixels[offset:offset + 4] = bytes([255, 0, 0, 255])
```

Note that the byte order depends on the _format_ returned, consistent with the
endian note above.

### XPM and PNG images

The **mlx_xpm_file_to_image**() and **mlx_png_file_to_image**() functions will
create a new image the same way. They will fill it using the specified
_filename_ . Note that
MiniLibX does not use the standard Xpm and PNG libraries to deal with xpm and
PNG images.

You may not be able to read all types of xpm and PNG images. It does, however,
handle transparency.

**mlx_xpm_to_image()** is not implemented in the Python wrapper as it is
considered not useful in this context.

### Return values

**mlx_new_image()** returns None if an error occurs, otherwise a non-null
integer as an image identifier. **mlx_xpm_file_to_image()** and
**mlx_png_file_to_image()** return a tuple ( _image_ , _width_ , _height_ ):
_image_ is None on error, otherwise a non-null integer image identifier.

## Handle events

### Synopsis

```python
def mlx_loop(mlx_ptr: int | None) -> int:

def mlx_key_hook(win_ptr: int | None, callback: Callable[..., Any] | None, param: Any) -> int:

def mlx_mouse_hook(win_ptr: int | None, callback: Callable[..., Any] | None, param: Any) -> int:

def mlx_expose_hook(win_ptr: int | None, callback: Callable[..., Any] | None, param: Any) -> int:

def mlx_loop_hook(mlx_ptr: int | None, callback: Callable[..., Any] | None, param: Any) -> int:

def mlx_hook(win_ptr: int | None, x_event: int, x_mask: int, callback: Callable[..., Any] | None, param: Any) -> int:

def mlx_loop_exit(mlx_ptr: int | None) -> int:
```

### Events

The graphical system is bi-directional. On one hand, the program sends orders to
the screen to display pixels, images, and so on. On the other hand, it can get
information from the keyboard and mouse associated to the screen. To do so, the
program receives "events" from the keyboard or the mouse.

### Description

To receive events, you must use **mlx_loop**(). This function never returns,
unless **mlx_loop_exit** is called. It is an infinite loop that waits for an
event, and then calls a user-defined function associated with this event. A
single parameter is needed, the connection identifier _mlx_ptr_.

![The event loop dispatches incoming key, mouse and expose events to the callbacks you registered.](media/diagram-event-loop.svg)

You can assign different functions to the three following events:

- A key is released
- The mouse button is pressed
- A part of the window should be re-drawn (this is called an "expose" event, and
  it is your program's job to handle it in the Unix/Linux X11 environment, but
  at the opposite it never happens on Unix/Linux Wayland-Vulkan nor on macOS).

Each window can define a different function for the same event.

The three functions **mlx_key_hook**(), **mlx_mouse_hook**() and
**mlx_expose_hook**() work exactly the same way. _callback_ is a reference to
the function that is invoked when an event occurs. This assignment is specific
to the window defined by the _win_ptr_ identifier. The _param_ address will be
passed back to your function every time it is called, and should be used to
store the parameters it might need.

The syntax for the **mlx_loop_hook**() function is similar to the previous
ones, but the given function will be called when no event occurs, and is not
bound to a specific window.

When it catches an event, the MiniLibX calls the corresponding function with
fixed parameters:

```c
expose_hook(void *param);
key_hook(unsigned int keycode, void *param);
mouse_hook(unsigned int button, unsigned int x, unsigned int y, void *param);
loop_hook(void *param);
```

These function names are arbitrary. They here are used to distinguish parameters
according to the event. These functions are NOT part of the MiniLibX.

_param_ is the address specified in the mlx\_\*\_hook calls. This address is
never used nor modified by the MiniLibX. On key and mouse events, additional
information is passed: _keycode_ tells you which key was released (we list the
common keycodes just below), ( _x_ , _y_ ) are the coordinates of the mouse
click in the window, and _button_ tells you which mouse button was pressed.

### Callbacks in Python

| Hook            | Callback signature                  |
| --------------- | ----------------------------------- |
| mlx_key_hook    | key_callback(keycode, param)        |
| mlx_mouse_hook  | mouse_callback(button, x, y, param) |
| mlx_expose_hook | expose_callback(param)              |
| mlx_loop_hook   | loop_callback(param)                |

The _param_ argument is the same Python object you passed when registering the
hook: the wrapper keeps it and gives it back to you on every call. The return
value of the callback is ignored. To remove a hook, call the same function again
with `None` as the callback.

Keycodes follow the X11 keysym convention: the space bar is 32, and special keys
such as Escape (0xFF1B), Return (0xFF0D) or the arrow keys (0xFF51-0xFF54) keep
the same values on the three platforms (XCB, Wayland via xkb, macOS via a
translation table). The package does not define key constants, so print the
_keynum_ to discover the values.

### Going further with events

The MiniLibX provides a much more generic access to other available events. The
_mlx.h_ include defines **mlx_hook()** in the same manner mlx\_\*\_hook functions
work. The event and mask values will be taken from the historical X11 include
file \"X.h\". Some Wayland and macOS events are mapped to these values when it
makes sense, and the mask may not be used in some configurations.

See source code of the MiniLibX to find out how it will call your own function
for a specific event.

The Python wrapper also exposes **mlx_hook**(_win_ptr_ , _x_event_ , _x_mask_ ,
_callback_ , _param_ ). The signature of the callback depends on _x_event_ :
key events [2, 3] receive ( _keycode_ , _param_ ), mouse events [4, 5] receive
( _button_ , _x_ , _y_ , _param_ ), motion events [6] receive ( _x_ , _y_ ,
_param_ ), and every other event receives only ( _param_ ,). The mask can be
ignored in some configurations.

## Extra functions

### Synopsis

```python
def mlx_mouse_hide(mlx_ptr: int | None) -> int:

def mlx_mouse_show(mlx_ptr: int | None) -> int:

def mlx_mouse_move(win_ptr: int | None, x: int, y: int) -> int:

def mlx_mouse_get_pos(win_ptr: int | None) -> tuple[int, int, int]: # (status, x, y)

def mlx_do_key_autorepeatoff(mlx_ptr: int | None) -> int:

def mlx_do_key_autorepeaton(mlx_ptr: int | None) -> int:

def mlx_get_screen_size(mlx_ptr: int | None) -> tuple[int, int, int]: # (status, width, height)

def mlx_do_sync(mlx_ptr: int | None) -> int:

def mlx_sync(mlx_ptr: int | None, cmd: int, img_or_win_ptr: int | None) -> int:
```

| Parameter      | Type | Description                                                                                    |
| -------------- | ---- | ---------------------------------------------------------------------------------------------- |
| mlx_ptr        | int  | Connection identifier returned by `mlx_init()`.                                                |
| win_ptr        | int  | Window identifier returned by `mlx_new_window()`.                                              |
| x, y           | int  | Coordinates inside the window.                                                                 |
| cmd            | int  | One of the `Mlx.SYNC_*` constants (see [Flush and sync functions](#flush-and-sync-functions)). |
| img_or_win_ptr | int  | Image or window identifier, depending on `cmd`.                                                |

### Example

```python
status, w, h = m.mlx_get_screen_size(mlx_ptr)
print(f"Screen is {w} x {h}")

m.mlx_mouse_hide(mlx_ptr)
m.mlx_mouse_move(win_ptr, w // 2, h // 2)
m.mlx_do_sync(mlx_ptr)
```

### Mouse extra functions

It is possible to show / hide the mouse, and get its current position without
user click or force its position inside a window.

**mlx_mouse_get_pos**() returns ( _status_ , _x_ , _y_ ): _status_ is 0 on
success and -1 on failure.

### Keyboard extra functions

The auto-repeat mode of the keyboard can be controlled. By default, auto-repeat
is on: while a key is held, multiple key events are generated until the key is
released.

### Screen extra function

It is possible to retrieve the size of the current screen, even before the first
window is created.

**mlx_get_screen_size**() returns ( _status_ , _width_ , _height_ ): _status_ is
always 0.

### Flush and sync functions

The **mlx_do_sync** function will flush the pending commands to the graphic
subsystems, ensuring nothing is cached on your software's side. On return, there
is no guarantee that your commands have been processed.

With **mlx_sync** you have more detailed control over the synchronisation
mechanisms. Three different commands are available:

- Mlx.SYNC_IMAGE_WRITABLE = 1
- Mlx.SYNC_WIN_FLUSH = 2
- Mlx.SYNC_WIN_COMPLETED = 3

The third parameter _param_ can be either the image identifier or the window
identifier. Note that these are class attributes of **Mlx** (not importable at
module level).
