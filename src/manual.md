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

> [!NOTE]
> New to graphics programming? You can read this manual as a short course
> instead of a dictionary: 1) [Getting started](#getting-started) to install
> the library and open your first window, 2) [Drawing inside
> windows](#drawing-inside-windows) and [Manipulating
> images](#manipulating-images) to put pixels on screen, 3) [Handle
> events](#handle-events) to react to the keyboard and the mouse, 4) the game
> loop in [Example of use](#example-of-use) to animate everything, and 5) test
> yourself with the exercises in [Try it yourself](#try-it-yourself). If you
> already know the API, jump straight to the [Function
> index](#function-index).

For background on how graphics servers handle windows and input, see
[Appendix A](#appendix-a-how-a-graphics-server-works).

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

![The life of a MiniLibX program: Mlx() and mlx_init() open the connection, mlx_new_window() opens the window, and mlx_loop() then takes over and never returns on its own, so mlx_loop_exit() is the way out.](media/diagram-lifecycle.svg)

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

Think of the window as a spreadsheet made of pixels: columns are _x_, rows
are _y_, and the first cell is (0, 0) in the top-left corner. Writing a pixel
means filling in one cell; anything drawn beyond the last cell is simply
ignored.

#### What happens when you draw a pixel

It helps to know what a single call sets in motion:

1. Your Python call crosses into the C library through ctypes.
2. MiniLibX turns `(x, y, color)` into the drawing primitive of the active
   backend: an X11 request, a Wayland buffer write, or a CoreGraphics call.
3. The backend hands it to the display server, which composites it into the
   window you see on screen.
4. Control comes back to your program, ready for the next call.

Steps 2 to 4 happen for **every single pixel**. That is the price of drawing
this way: filling a 640×480 window takes over 300 000 individual calls, each
one talking to the graphics system. [Manipulating
images](#manipulating-images) replaces all of them with a single call.

### Color management

The _color_ parameter has an unsigned integer type. The displayed color needs
to be encoded in this integer, following a defined scheme. All displayable
colors can be split in 3 basic colors: red, green and blue. Three associated
values, in the 0-255 range, represent how much of each color is mixed up to
create the original color. The fourth byte is the alpha channel: 0 means fully
transparent and 255 fully opaque.

> [!NOTE]
> The fourth byte is an **opacity** channel following the GPU standard (0 fully
> transparent, 255 opaque). Historically MiniLibX used it the other way round,
> as a transparency value; that is no longer the case. Also note that
> **mlx_string_put**() forces this byte to 255, so the text it draws is always
> fully opaque.

These four values must be set inside the unsigned integer to display the right
color. The bytes of this integer are filled in 32-bit color packing (little-endian), as shown in the picture below:

![A color is packed into a 32-bit integer as four bytes: blue, green, red and alpha.](media/diagram-color-bytes.svg)

While filling the integer, make sure you avoid endian problems.

Example: the "blue" byte will be the least significant byte inside the integer
on a little endian machine.

In practice, you rarely juggle bytes by hand: build the integer with shifts,
and let Python do the packing:

```python
def rgba(r, g, b, a=255):
    return (a << 24) | (r << 16) | (g << 8) | b

red = rgba(255, 0, 0)          # 0xFFFF0000
semi_blue = rgba(0, 0, 255, 128)  # 0x800000FF
```

To recover the channels from a packed color, shift the other way:

```python
a = (color >> 24) & 0xFF
r = (color >> 16) & 0xFF
g = (color >> 8) & 0xFF
b = color & 0xFF
```

| You want        | `rgba()` call          | Integer      | Bytes in memory (format 0) |
| --------------- | ---------------------- | ------------ | -------------------------- |
| Red, opaque     | `rgba(255, 0, 0)`      | `0xFFFF0000` | `00 00 FF FF`              |
| Green, opaque   | `rgba(0, 255, 0)`      | `0xFF00FF00` | `00 FF 00 FF`              |
| Blue, opaque    | `rgba(0, 0, 255)`      | `0xFF0000FF` | `FF 00 00 FF`              |
| Blue, 50% alpha | `rgba(0, 0, 255, 128)` | `0x800000FF` | `FF 00 00 80`              |

Try to guess before looking at the answers: `0xFF00FF00` is opaque green,
`0x80FF0000` is red at 50% alpha.

One last subtlety: `mlx_pixel_put()` and `mlx_string_put()` take the packed
integer, but when you write pixels through the `memoryview` returned by
`mlx_get_data_addr()` you are writing **raw bytes**; there you assign
`bytes([blue, green, red, alpha])` directly (see [Storing colors inside
images](#storing-colors-inside-images)). The integer and the bytes are the
same color seen from two different levels.

_In one sentence:_ a color is just a 32-bit number: pack it with `rgba()`
for `mlx_pixel_put()`, or write its four bytes directly into an image buffer.

## Manipulating images

Drawing pixel by pixel into the window is slow, because every call has to
talk to the graphics system. Images solve this: you draw into an off-screen
buffer (a canvas that lives in memory) and then stamp the whole picture
onto the window in a single call. This is the technique every real MiniLibX
project uses.

Why is it so much better? Two reasons. First, one trip to the graphics
system instead of thousands. Second, and just as important: the user never
sees your half-finished drawing. You paint the complete frame in private and
only show it when it is done, like writing a full page before turning it
around. If you drew straight onto the visible window, every intermediate
pixel would be visible (flickering included). This technique has a name:
double buffering, because you keep the visible picture and your private
canvas as two separate buffers.

### Synopsis

```python
def mlx_new_image(mlx_ptr: int | None, width: int, height: int) -> int | None: # void *

def mlx_get_data_addr(img_ptr: int | None) -> tuple[memoryview, int, int, int]: # (pixels, bits_per_pixel, size_line, format)

def mlx_put_image_to_window(mlx_ptr: int | None, win_ptr: int | None, img_ptr: int | None, x: int, y: int) -> int:

def mlx_xpm_file_to_image(mlx_ptr: int | None, filename: str) -> tuple[int | None, int, int]: # (image: void *, width, height)

def mlx_png_file_to_image(mlx_ptr: int | None, filename: str) -> tuple[int | None, int, int]: # (image: void *, width, height)

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
pixel color (also called the depth of the image). _size_line_ is the number of
bytes used to store one line of the image in memory (the stride); this
information is needed to move from one line to another in the image. _format_
tells you how each pixel color in the image is structured.

Currently only 2 values are defined:

- 0 means format B8G8R8A8
- 1 means format A8R8G8B8

The offset of a pixel is computed as
`offset = y * size_line + x * (bits_per_pixel // 8)`; the following 4 bytes are
the color of that pixel.

> [!WARNING]
> Always index pixels through `size_line`, never through `width * 4`. It is
> the stride (bytes per row), and it is the portable way to walk a buffer.
> In this library the Vulkan renderer currently sets it to exactly
> `width * 4` (no padding), but writing your offsets as `y * size_line +
x * (bits_per_pixel // 8)` keeps the code correct even if that ever
> changes, and matches how the value is meant to be used. Computing offsets
> with `width * 4` is the classic bug that makes pixels land diagonally.

![A framebuffer row is six 4-byte pixels followed by 8 padding bytes, so size_line is 32 bytes instead of 24; the pixel at (2, 1) starts at offset 1 × 32 + 2 × 4 = 40.](media/diagram-stride.svg)

A concrete example: a 300-pixel-wide image has 1200 bytes of pixel data per
row, but `size_line` may be 1216 (1200 plus 16 bytes of padding). The pixel
at (2, 1) then lives at `offset = 1 * 1216 + 2 * 4 = 1224`, not at
`1 * 1200 + 2 * 4 = 1208`.

**mlx_destroy_image** destroys the given image ( _img_ptr_ ).

### Storing colors inside images

Depending on the graphic system, the number of bits used to store a pixel color
used to be different from one hardware to another. Today, the way the user
usually represents a color, in the ARGB mode, almost always matches the
hardware capabilities on modern computers.

The color packing rules described in [Color management](#color-management)
apply here too, and they depend on the local computer's endianness; adjust your
code accordingly.

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

> [!WARNING]
> If you rewrite the buffer of an image that is already on screen, tell
> MiniLibX you are done before drawing the next frame, with
> `m.mlx_sync(mlx_ptr, m.SYNC_IMAGE_WRITABLE, img_ptr)`. Skipping this can
> leave visible artifacts while the graphics card is still reading the buffer.

### XPM and PNG images

The **mlx_xpm_file_to_image**() and **mlx_png_file_to_image**() functions will
create a new image the same way. They will fill it using the specified
_filename_ . Note that
MiniLibX does not use the standard Xpm and PNG libraries to deal with xpm and
PNG images.

You may not be able to read all types of xpm and PNG images. It does, however,
handle transparency.

> [!NOTE]
> The built-in loaders are limited. PNG: only 8- or 16-bit images of color
> type 2 (RGB) or 6 (RGBA), without interlacing; an indexed PNG (for example
> exported by GIMP) fails and returns `None`. The PNG loader swaps the red and
> blue channels for you, so the result matches the BGRA format of everything
> else. XPM: the parser understands the standard X11 color names (like `red`
> or `tomato`), `#RRGGBB` values, and `none` for transparent pixels.

**mlx_xpm_to_image()** is not implemented in the Python wrapper as it is
considered not useful in this context.

### Return values

**mlx_new_image()** returns None if an error occurs, otherwise a non-null
integer as an image identifier. **mlx_xpm_file_to_image()** and
**mlx_png_file_to_image()** return a tuple ( _image_ , _width_ , _height_ ):
_image_ is None on error, otherwise a non-null integer image identifier.

_In one sentence:_ draw into the off-screen image, then show it in one
`mlx_put_image_to_window()`, and always walk it with `size_line`, never with
`width * 4`.

## Handle events

A window that never reacts is just a screensaver. This section covers the
event loop: the mechanism that delivers keyboard and mouse input to your
program. Think of `mlx_loop()` as a receptionist: it waits at the desk,
hands every event to the callback you registered for it, and calls your
`mlx_loop_hook()` function whenever the desk is quiet.

This changes how you program: your code becomes **event-driven**. You do not
write one long `while True:` that asks "any key pressed?" in a circle;
instead you register small functions and go to sleep. MiniLibX wakes the
right one when something actually happens. After `mlx_loop()` starts, the
only code that runs is your callbacks. That is why the order of calls in the
examples matters: hooks must be registered before the loop begins.

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

> [!IMPORTANT]
> `mlx_key_hook()` fires when a key is **released**, not when it is pressed.
> To react to key presses you need the generic `mlx_hook()` with the KeyPress
> event (number 2); see [Going further with events](#going-further-with-events).

The syntax for the **mlx_loop_hook**() function is similar to the previous
ones, but the given function is called on **every iteration** of `mlx_loop()`
(once per frame, right before events are checked) rather than when a specific
event fires, and it is not bound to a specific window.

When it catches an event, the MiniLibX calls the corresponding function with
fixed parameters. Under the hood, everything is an X11 event with a number,
and the convenience hooks are just shortcuts for the most common ones:

| X11 event     | Number | Callback parameters     | Convenience hook     |
| ------------- | ------ | ----------------------- | -------------------- |
| KeyPress      | 2      | `(keycode, param)`      | (none)               |
| KeyRelease    | 3      | `(keycode, param)`      | `mlx_key_hook`       |
| ButtonPress   | 4      | `(button, x, y, param)` | `mlx_mouse_hook`     |
| ButtonRelease | 5      | `(button, x, y, param)` | (none)               |
| MotionNotify  | 6      | `(x, y, param)`         | (none)               |
| Expose        | 12     | `(param,)`              | `mlx_expose_hook`    |
| ClientMessage | 33     | `(param,)`              | (none), window close |

_param_ is the address specified in the `mlx_*_hook` calls. This address is
never used nor modified by the MiniLibX. On key and mouse events, additional
information is passed: _keycode_ tells you which key was released (we list the
common keysyms just below), ( _x_ , _y_ ) are the coordinates of the mouse
click in the window, and _button_ tells you which mouse button was pressed.

#### What happens when you press a key

Following one keypress from the hardware to your own code makes the whole
design click:

1. The keyboard sends a scan code to the operating system.
2. The display server turns it into a key event carrying a **keycode** (which
   physical key) and a **keysym** (which character).
3. MiniLibX receives the event and looks up the callback you registered for
   KeyPress (event 2).
4. It calls your callback as `callback(keycode, param)`.
5. Your function updates your own state and returns immediately.
6. `mlx_loop()` goes back to waiting for the next event.

Step 5 is the idea worth remembering: the callback changes variables, it does
not draw. The drawing happens once per frame in the loop hook. That is the
game loop you will write in [Try it yourself](#try-it-yourself).

### Callbacks in Python

| Hook            | Callback signature                  |
| --------------- | ----------------------------------- |
| mlx_key_hook    | key_callback(keycode, param)        |
| mlx_mouse_hook  | mouse_callback(button, x, y, param) |
| mlx_expose_hook | expose_callback(param)              |
| mlx_loop_hook   | loop_callback(param)                |

The _param_ argument is the same Python object you passed when registering the
hook: the wrapper keeps it and gives it back to you on every call. The return
value of the callback is ignored, and the registration functions themselves
return `0`. To remove a **convenience** hook (`mlx_key_hook`, `mlx_mouse_hook`,
`mlx_loop_hook`, ...), call the same function again with `None` as the
callback. This does _not_ work for the generic `mlx_hook`: passing `None`
there is forwarded internally with the wrong event and mask, so it fails to
clear the slot you registered. To stop responding to a raw event, keep the
hook registered but make its callback do nothing; the event will still be
delivered but ignored.

For games you usually want to know which keys are held _right now_. The
pattern is: turn auto-repeat off, track presses and releases in a `set`, and
read that set every frame:

```python
pressed = set()

m.mlx_do_key_autorepeatoff(mlx_ptr)
m.mlx_hook(win_ptr, 2, 1, lambda k, p: pressed.add(k), None)      # KeyPress
m.mlx_hook(win_ptr, 3, 2, lambda k, p: pressed.discard(k), None)  # KeyRelease
```

The set-based pattern is also robust on Wayland, where the auto-repeat
functions may be no-ops, because it does not rely on repeated events.

Key values follow the X11 keysym convention: the space bar is 32, and special keys
such as Escape (0xFF1B), Return (0xFF0D) or the arrow keys (0xFF51-0xFF54) keep
the same values on the three platforms (XCB, Wayland via xkb, macOS via a
translation table). The package does not define key constants, so print the
_keynum_ to discover the values. Here are the most common ones:

| Key                      | Keysym        | Decimal     |
| ------------------------ | ------------- | ----------- |
| Space                    | 0x20          | 32          |
| Digits `0`–`9`           | 0x30–0x39     | 48–57       |
| Letters `a`–`z`          | 0x61–0x7A     | 97–122      |
| Backspace                | 0xFF08        | 65288       |
| Tab                      | 0xFF09        | 65289       |
| Return                   | 0xFF0D        | 65293       |
| Escape                   | 0xFF1B        | 65307       |
| Home                     | 0xFF50        | 65360       |
| Left / Up / Right / Down | 0xFF51–0xFF54 | 65361–65364 |
| Page Up                  | 0xFF55        | 65365       |
| Page Down                | 0xFF56        | 65366       |
| End                      | 0xFF57        | 65367       |
| Delete                   | 0xFFFF        | 65535       |

> [!WARNING]
> The `keynum` you receive is an X11 **keysym**, not a physical keycode: for
> printable characters it simply matches the ASCII code (`a` is 97, `A` is
> 65, `0` is 48). Do not copy raw X11 keycode tables into your program; they
> use completely different numbers.

The complete keysym tables, together with every X11 event number and event
mask, are collected in [Appendix B](#appendix-b-keysyms-events-and-masks).

### Going further with events

The MiniLibX provides a much more generic access to other available events. The
_mlx.h_ include defines **mlx_hook()** in the same manner `mlx_*_hook` functions
work. The event and mask values will be taken from the historical X11 include
file "X.h". Some Wayland and macOS events are mapped to these values when it
makes sense, and the mask may not be used in some configurations.

See source code of the MiniLibX to find out how it will call your own function
for a specific event.

The Python wrapper also exposes **mlx_hook**(_win_ptr_ , _x_event_ , _x_mask_ ,
_callback_ , _param_ ). The signature of the callback depends on _x_event_ :
key events [2, 3] receive ( _keycode_ , _param_ ), mouse events [4, 5] receive
( _button_ , _x_ , _y_ , _param_ ), motion events [6] receive ( _x_ , _y_ ,
_param_ ), and every other event receives only ( _param_ ,). The mask can be
ignored in some configurations.

A common use is the title-bar close button: event 33 (`WM_DELETE_WINDOW`)
fires when the user clicks it, and the usual response is to leave the loop:

```python
def on_close(param):
    m.mlx_loop_exit(mlx_ptr)

m.mlx_hook(win_ptr, 33, 0, on_close, None)
```

The full lists of event numbers, event masks and keysyms live in
[Appendix B](#appendix-b-keysyms-events-and-masks).

_In one sentence:_ register your callbacks before `mlx_loop()`, remember that
`mlx_key_hook()` fires on release (event 2 is the press), and the loop will
deliver everything from there.

## Extra functions

Everything that did not fit anywhere else: mouse cursor tricks, keyboard
auto-repeat, screen size, and explicit synchronization with the graphics
system.

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

With **mlx_sync** you have more detailed control over the synchronization
mechanisms. Three different commands are available:

- Mlx.SYNC_IMAGE_WRITABLE = 1
- Mlx.SYNC_WIN_FLUSH = 2
- Mlx.SYNC_WIN_COMPLETED = 3

The third parameter _img_or_win_ptr_ can be either the image identifier or the
window identifier. Note that these are class attributes of **Mlx** (not
importable at module level).

### Platform differences

MiniLibX sits on top of three different backends, and a few behaviors change
between them. If your program works on one machine but not on another, check
this table before blaming your code:

| Behavior                     | X11 (Linux)                 | Wayland (Linux)             | macOS (AppKit)         |
| ---------------------------- | --------------------------- | --------------------------- | ---------------------- |
| Expose events                | Once, usually               | Once, after first show      | Once, after first show |
| `mlx_do_key_autorepeatoff()` | Works                       | May be a no-op              | Filters the OS repeat  |
| `mlx_mouse_move()`           | Works                       | May return `-1`             | Works                  |
| Content before `mlx_loop()`  | Shown after `mlx_do_sync()` | Shown after `mlx_do_sync()` | Nothing is shown       |

## Try it yourself

Reading is not enough: the only way to learn a graphics library is to make
pixels obey you. The five exercises below build on each other and only use
what this manual has covered. Try each one on your own before looking at the
solution.

### 1. Your first window

Open a 640×480 window titled with your login, and make Escape close the
program cleanly. Don't forget the `None` checks.

```python
from mlx import Mlx

m = Mlx()
mlx_ptr = m.mlx_init()
if mlx_ptr is None:
    raise RuntimeError("mlx_init() failed")
win_ptr = m.mlx_new_window(mlx_ptr, 640, 480, "your_login")


def on_key(keycode, param):
    if keycode == 65307:  # Escape
        m.mlx_loop_exit(mlx_ptr)


m.mlx_hook(win_ptr, 2, 1, on_key, None)  # event 2 = KeyPress
m.mlx_loop(mlx_ptr)
m.mlx_destroy_window(mlx_ptr, win_ptr)
m.mlx_release(mlx_ptr)
```

### 2. A gradient

Fill the window with a gradient that goes from black (top) to blue (bottom).
First do it with `mlx_pixel_put()` in a loop. Then do it again with an image
buffer and a single `mlx_put_image_to_window()`. Notice the speed difference:
that is why images exist.

```python
from mlx import Mlx

m = Mlx()
mlx_ptr = m.mlx_init()
win_ptr = m.mlx_new_window(mlx_ptr, 640, 480, "Gradient")


def rgba(r, g, b, a=255):
    return (a << 24) | (r << 16) | (g << 8) | b


# Slow version: one call to the graphics system per pixel
for y in range(480):
    for x in range(640):
        m.mlx_pixel_put(mlx_ptr, win_ptr, x, y, rgba(0, 0, y // 2))

# Fast version: one buffer, one blit
img_ptr = m.mlx_new_image(mlx_ptr, 640, 480)
pixels, bpp, size_line, fmt = m.mlx_get_data_addr(img_ptr)
for y in range(480):
    for x in range(640):
        offset = y * size_line + x * 4
        pixels[offset:offset + 4] = bytes([y // 2, 0, 0, 255])  # BGRA
m.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)
m.mlx_loop(mlx_ptr)
m.mlx_destroy_image(mlx_ptr, img_ptr)
m.mlx_destroy_window(mlx_ptr, win_ptr)
m.mlx_release(mlx_ptr)
```

### 3. Key spy

Print the keysym of every key you press (you need event 2) and exit with
Escape. Then hold a letter key down: how many events do you get? Call
`mlx_do_key_autorepeatoff()` and compare.

```python
from mlx import Mlx

m = Mlx()
mlx_ptr = m.mlx_init()
win_ptr = m.mlx_new_window(mlx_ptr, 300, 200, "Key spy")


def on_press(keycode, param):
    print(f"key {keycode} (0x{keycode:X})")
    if keycode == 65307:  # Escape
        m.mlx_loop_exit(mlx_ptr)


m.mlx_do_key_autorepeatoff(mlx_ptr)  # remove this line to compare
m.mlx_hook(win_ptr, 2, 1, on_press, None)
m.mlx_loop(mlx_ptr)
m.mlx_destroy_window(mlx_ptr, win_ptr)
m.mlx_release(mlx_ptr)
```

### 4. Moving square

A 40×40 square that moves at a constant speed with the arrow keys (or WASD).
Use the framebuffer pattern and `time.monotonic()` so the speed does not
depend on how fast your computer is.

```python
import time

from mlx import Mlx

W, H = 640, 480
SIZE = 40
m = Mlx()
mlx_ptr = m.mlx_init()
win_ptr = m.mlx_new_window(mlx_ptr, W, H, "Moving square")
img_ptr = m.mlx_new_image(mlx_ptr, W, H)
pixels, bpp, size_line, fmt = m.mlx_get_data_addr(img_ptr)

x, y = W // 2 - SIZE // 2, H // 2 - SIZE // 2
pressed = set()
last = time.monotonic()


def put_square(px, py):
    for row in range(SIZE):
        for col in range(SIZE):
            off = (py + row) * size_line + (px + col) * 4
            pixels[off:off + 4] = bytes([0, 0, 255, 255])  # BGRA red


def frame(param):
    global last, x, y
    now = time.monotonic()
    dt = now - last
    last = now
    m.mlx_sync(mlx_ptr, m.SYNC_IMAGE_WRITABLE, img_ptr)
    pixels[:] = b"\x00" * len(pixels)
    if 65361 in pressed or 97 in pressed:    # Left / A
        x -= 200 * dt
    if 65363 in pressed or 100 in pressed:   # Right / D
        x += 200 * dt
    if 65362 in pressed or 119 in pressed:   # Up / W
        y -= 200 * dt
    if 65364 in pressed or 115 in pressed:   # Down / S
        y += 200 * dt
    x = max(0, min(W - SIZE, x))
    y = max(0, min(H - SIZE, y))
    put_square(int(x), int(y))
    m.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)


m.mlx_do_key_autorepeatoff(mlx_ptr)
m.mlx_hook(win_ptr, 2, 1, lambda k, p: pressed.add(k), None)
m.mlx_hook(win_ptr, 3, 2, lambda k, p: pressed.discard(k), None)
m.mlx_loop_hook(mlx_ptr, frame, None)
m.mlx_loop(mlx_ptr)
m.mlx_destroy_image(mlx_ptr, img_ptr)
m.mlx_destroy_window(mlx_ptr, win_ptr)
m.mlx_release(mlx_ptr)
```

### 5. Bouncing square

Same square, but it bounces off the window edges, and its color changes with
its position on screen. When this works, you have everything you need for
your first 42 graphics project.

```python
import time

from mlx import Mlx

W, H = 640, 480
SIZE = 40
m = Mlx()
mlx_ptr = m.mlx_init()
win_ptr = m.mlx_new_window(mlx_ptr, W, H, "Bouncing square")
img_ptr = m.mlx_new_image(mlx_ptr, W, H)
pixels, bpp, size_line, fmt = m.mlx_get_data_addr(img_ptr)

x, y = W / 2, H / 2
vx, vy = 300.0, 220.0  # pixels per second
last = time.monotonic()


def frame(param):
    global last, x, y, vx, vy
    now = time.monotonic()
    dt = now - last
    last = now
    x += vx * dt
    y += vy * dt
    if x <= 0 or x >= W - SIZE:
        vx = -vx
        x = max(0, min(W - SIZE, x))
    if y <= 0 or y >= H - SIZE:
        vy = -vy
        y = max(0, min(H - SIZE, y))
    m.mlx_sync(mlx_ptr, m.SYNC_IMAGE_WRITABLE, img_ptr)
    pixels[:] = b"\x00" * len(pixels)
    r = int(255 * x / W)  # the color follows the position
    g = int(255 * y / H)
    for row in range(SIZE):
        for col in range(SIZE):
            off = (int(y) + row) * size_line + (int(x) + col) * 4
            pixels[off:off + 4] = bytes([0, g, r, 255])  # BGRA
    m.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)


m.mlx_loop_hook(mlx_ptr, frame, None)
m.mlx_loop(mlx_ptr)
m.mlx_destroy_image(mlx_ptr, img_ptr)
m.mlx_destroy_window(mlx_ptr, win_ptr)
m.mlx_release(mlx_ptr)
```

## Troubleshooting

| Symptom                                  | Likely cause                                                 | Fix                                                                        |
| ---------------------------------------- | ------------------------------------------------------------ | -------------------------------------------------------------------------- |
| `Ctrl-C` does not stop the program       | Some backends only notice signals while idle in `mlx_loop()` | Install a `SIGINT` handler that calls `mlx_loop_exit()`, or press `Ctrl-\` |
| `mlx_init()` returns `None`              | No display or missing backend                                | Check your environment and dependencies                                    |
| `import mlx` fails to load `libmlx`      | Wrong wheel or missing library                               | Reinstall a wheel built for your platform                                  |
| `pip install` of an intra `.whl` fails   | Non-standard filename                                        | Rename it to `mlx-2.4-py3-none-any.whl`                                    |
| `mlx_png_file_to_image()` returns `None` | Unsupported PNG variant                                      | Use 8/16-bit RGB or RGBA, non-indexed                                      |
| Window or image identifier is `None`     | Creation failed silently                                     | Check every creation result                                                |
| Window opens but stays black             | Nothing is drawn from the loop                               | Draw from `mlx_loop_hook()` every frame                                    |
| Callbacks never fire                     | Hooks registered too late                                    | Register hooks before calling `mlx_loop()`                                 |
| Key only reacts when released            | `mlx_key_hook()` fires on release                            | Use `mlx_hook(win, 2, ...)` for presses                                    |
| Pixels land diagonally                   | Offsets computed with `width * 4`                            | Use `size_line` (the stride)                                               |
| Artifacts when updating an image         | Buffer rewritten without sync                                | Call `mlx_sync(mlx_ptr, m.SYNC_IMAGE_WRITABLE, img_ptr)`                   |
| Nothing shows on macOS                   | Nothing drawn once `mlx_loop()` is running                   | Draw from `mlx_loop_hook()`                                                |
| `mlx_mouse_move()` returns `-1`          | Wayland backend limitation                                   | Accept the failure or check the backend                                    |
| `ValueError` when unpacking a result     | Tuples start with a `status` element                         | Unpack it: `status, w, h = ...`                                            |

## Function index

Every function exposed by the Python wrapper, grouped by the section that
documents it.

| Function                                                                                                                               | Section                                                   |
| -------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| `mlx_init`, `mlx_release`                                                                                                              | [Initialization and cleanup](#initialization-and-cleanup) |
| `mlx_new_window`, `mlx_clear_window`, `mlx_destroy_window`                                                                             | [Managing windows](#managing-windows)                     |
| `mlx_pixel_put`, `mlx_string_put`                                                                                                      | [Drawing inside windows](#drawing-inside-windows)         |
| `mlx_new_image`, `mlx_get_data_addr`, `mlx_put_image_to_window`, `mlx_destroy_image`, `mlx_xpm_file_to_image`, `mlx_png_file_to_image` | [Manipulating images](#manipulating-images)               |
| `mlx_loop`, `mlx_loop_exit`, `mlx_key_hook`, `mlx_mouse_hook`, `mlx_expose_hook`, `mlx_loop_hook`, `mlx_hook`                          | [Handle events](#handle-events)                           |
| `mlx_mouse_hide`, `mlx_mouse_show`, `mlx_mouse_move`, `mlx_mouse_get_pos`                                                              | [Extra functions](#extra-functions)                       |
| `mlx_do_key_autorepeatoff`, `mlx_do_key_autorepeaton`                                                                                  | [Extra functions](#extra-functions)                       |
| `mlx_get_screen_size`, `mlx_do_sync`, `mlx_sync`                                                                                       | [Extra functions](#extra-functions)                       |

## Appendix A: How a graphics server works

This library interacts with the underlying graphics system of your operating
system. Before diving into usage, it's helpful to understand how graphics
servers manage windows and handle user input.

### Unix/Linux: Historical X-Window concept

The X Window System, often called X11, is the software layer that draws text and graphics on the screen. X does not decide how applications look: that is the job of each X client, of a window manager such as Window Maker or Tab Window Manager, or of a complete desktop environment like KDE, GNOME or Xfce.

X is cross-platform: Linux, the BSDs, Solaris and other Unix-like systems all support it, and implementations exist for Apple’s macOS and Microsoft Windows as well.

It is based on two main parts:

- On one side, your software wants to draw something on the screen and/or get
  keyboard & mouse entries.

- On the other side, the X-Server manages the screen, keyboard and mouse (It is
  often referred to as a "display").

A network connection must be established between these two entities to send
drawing orders (from the software to the X-Server), and keyboard/mouse events
(from the X-Server to the software).

Nowadays, most of the time, both run on the same computer.

![The X Window System: applications are X clients, while the X server owns the display and sends input events back to the clients.](media/diagram-x11.svg)

### Unix/Linux: Wayland, the modern graphical approach

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

### MacOS: Window server and GPU

Your software interacts directly with the Window server that handles the cohabitation on the screen with other software and the event system, and interacts with the GPU to handle all drawing commands.

## Appendix B: Keysyms, events and masks

This appendix collects everything you may need to look up while writing
event code: the complete set of keysyms a physical keyboard can send, the
X11 event numbers passed to **mlx_hook**(), and the event masks it accepts.
All values come from the official X11 headers (`keysymdef.h` and `X.h`),
the same tables MiniLibX itself uses.

Keysym values are written in hexadecimal, as in the original headers.
Convert them when you need the decimal form with `int("0xFF51", 16)`, or
simply `print(keynum)` inside a key callback. Printable keys are plain
ASCII: `XK_a` = `0x61` = 97.

### X11 event numbers

The wrapper passes these numbers through unchanged, so they are what you
give as the _x_event_ argument of **mlx_hook**():

| X11 event        | Number | Python callback parameters |
| ---------------- | ------ | -------------------------- |
| KeyPress         | 2      | `(keycode, param)`         |
| KeyRelease       | 3      | `(keycode, param)`         |
| ButtonPress      | 4      | `(button, x, y, param)`    |
| ButtonRelease    | 5      | `(button, x, y, param)`    |
| MotionNotify     | 6      | `(x, y, param)`            |
| EnterNotify      | 7      | `(param,)`                 |
| LeaveNotify      | 8      | `(param,)`                 |
| FocusIn          | 9      | `(param,)`                 |
| FocusOut         | 10     | `(param,)`                 |
| KeymapNotify     | 11     | `(param,)`                 |
| Expose           | 12     | `(param,)`                 |
| GraphicsExpose   | 13     | `(param,)`                 |
| NoExpose         | 14     | `(param,)`                 |
| VisibilityNotify | 15     | `(param,)`                 |
| CreateNotify     | 16     | `(param,)`                 |
| DestroyNotify    | 17     | `(param,)`                 |
| UnmapNotify      | 18     | `(param,)`                 |
| MapNotify        | 19     | `(param,)`                 |
| MapRequest       | 20     | `(param,)`                 |
| ReparentNotify   | 21     | `(param,)`                 |
| ConfigureNotify  | 22     | `(param,)`                 |
| ConfigureRequest | 23     | `(param,)`                 |
| GravityNotify    | 24     | `(param,)`                 |
| ResizeRequest    | 25     | `(param,)`                 |
| CirculateNotify  | 26     | `(param,)`                 |
| CirculateRequest | 27     | `(param,)`                 |
| PropertyNotify   | 28     | `(param,)`                 |
| SelectionClear   | 29     | `(param,)`                 |
| SelectionRequest | 30     | `(param,)`                 |
| SelectionNotify  | 31     | `(param,)`                 |
| ColormapNotify   | 32     | `(param,)`                 |
| ClientMessage    | 33     | `(param,)`                 |
| MappingNotify    | 34     | `(param,)`                 |
| GenericEvent     | 35     | `(param,)`                 |

Only a subset of these reaches your program: the backend translates what
the platform can actually deliver (for example, X11 also generates
`GraphicsExpose` or `ReparentNotify`, which have no meaning in a typical
MiniLibX program).

### Event masks

The second argument of **mlx_hook**() is the _x_mask_: a bit flag that
tells the X11 server which events to deliver. Combine masks with `|`
when you need more than one:

| Mask                     | Value    |
| ------------------------ | -------- |
| NoEventMask              | 0        |
| KeyPressMask             | 1        |
| KeyReleaseMask           | 2        |
| ButtonPressMask          | 4        |
| ButtonReleaseMask        | 8        |
| EnterWindowMask          | 16       |
| LeaveWindowMask          | 32       |
| PointerMotionMask        | 64       |
| PointerMotionHintMask    | 128      |
| Button1MotionMask        | 256      |
| Button2MotionMask        | 512      |
| Button3MotionMask        | 1024     |
| Button4MotionMask        | 2048     |
| Button5MotionMask        | 4096     |
| ButtonMotionMask         | 8192     |
| KeymapStateMask          | 16384    |
| ExposureMask             | 32768    |
| VisibilityChangeMask     | 65536    |
| StructureNotifyMask      | 131072   |
| ResizeRedirectMask       | 262144   |
| SubstructureNotifyMask   | 524288   |
| SubstructureRedirectMask | 1048576  |
| FocusChangeMask          | 2097152  |
| PropertyChangeMask       | 4194304  |
| ColormapChangeMask       | 8388608  |
| OwnerGrabButtonMask      | 16777216 |

In practice, most programs only need the first four:
`KeyPressMask` (1), `KeyReleaseMask` (2), `ButtonPressMask` (4) and `ButtonReleaseMask` (8). The Wayland and macOS backends may ignore the mask.

### Key and button masks

These appear in the _state_ field of motion and button events, telling you
which modifier keys or buttons were held at that moment:

| Mask        | Value | Bit     |
| ----------- | ----- | ------- |
| ShiftMask   | 1     | 1 << 0  |
| LockMask    | 2     | 1 << 1  |
| ControlMask | 4     | 1 << 2  |
| Mod1Mask    | 8     | 1 << 3  |
| Mod2Mask    | 16    | 1 << 4  |
| Mod3Mask    | 32    | 1 << 5  |
| Mod4Mask    | 64    | 1 << 6  |
| Mod5Mask    | 128   | 1 << 7  |
| Button1Mask | 256   | 1 << 8  |
| Button2Mask | 512   | 1 << 9  |
| Button3Mask | 1024  | 1 << 10 |
| Button4Mask | 2048  | 1 << 11 |
| Button5Mask | 4096  | 1 << 12 |
| AnyModifier | 32768 | 1 << 15 |

### Keysym tables

Complete tables of every keysym a physical keyboard can produce, grouped
as in `keysymdef.h`. X11 also defines keysyms for other alphabets
(Katakana, Arabic, Cyrillic, Greek, Hebrew, Thai, Korean), for technical
and publishing symbols, and for Unicode characters above `0xFFFF`; those
are not listed here.

#### TTY function keys

| Key              | Keysym   | Key          | Keysym   |
| ---------------- | -------- | ------------ | -------- |
| `XK_BackSpace`   | `0xff08` | `XK_Tab`     | `0xff09` |
| `XK_Linefeed`    | `0xff0a` | `XK_Clear`   | `0xff0b` |
| `XK_Return`      | `0xff0d` | `XK_Pause`   | `0xff13` |
| `XK_Scroll_Lock` | `0xff14` | `XK_Sys_Req` | `0xff15` |
| `XK_Escape`      | `0xff1b` | `XK_Delete`  | `0xffff` |

#### Cursor keys

| Key            | Keysym   | Key        | Keysym   |
| -------------- | -------- | ---------- | -------- |
| `XK_Home`      | `0xff50` | `XK_Left`  | `0xff51` |
| `XK_Up`        | `0xff52` | `XK_Right` | `0xff53` |
| `XK_Down`      | `0xff54` | `XK_Prior` | `0xff55` |
| `XK_Page_Up`   | `0xff55` | `XK_Next`  | `0xff56` |
| `XK_Page_Down` | `0xff56` | `XK_End`   | `0xff57` |
| `XK_Begin`     | `0xff58` |            |          |

#### Misc function keys

| Key                | Keysym   | Key              | Keysym   |
| ------------------ | -------- | ---------------- | -------- |
| `XK_Select`        | `0xff60` | `XK_Print`       | `0xff61` |
| `XK_Execute`       | `0xff62` | `XK_Insert`      | `0xff63` |
| `XK_Undo`          | `0xff65` | `XK_Redo`        | `0xff66` |
| `XK_Menu`          | `0xff67` | `XK_Find`        | `0xff68` |
| `XK_Cancel`        | `0xff69` | `XK_Help`        | `0xff6a` |
| `XK_Break`         | `0xff6b` | `XK_Mode_switch` | `0xff7e` |
| `XK_script_switch` | `0xff7e` | `XK_Num_Lock`    | `0xff7f` |

#### Keypad

| Key              | Keysym   | Key               | Keysym   |
| ---------------- | -------- | ----------------- | -------- |
| `XK_KP_Space`    | `0xff80` | `XK_KP_Tab`       | `0xff89` |
| `XK_KP_Enter`    | `0xff8d` | `XK_KP_F1`        | `0xff91` |
| `XK_KP_F2`       | `0xff92` | `XK_KP_F3`        | `0xff93` |
| `XK_KP_F4`       | `0xff94` | `XK_KP_Home`      | `0xff95` |
| `XK_KP_Left`     | `0xff96` | `XK_KP_Up`        | `0xff97` |
| `XK_KP_Right`    | `0xff98` | `XK_KP_Down`      | `0xff99` |
| `XK_KP_Prior`    | `0xff9a` | `XK_KP_Page_Up`   | `0xff9a` |
| `XK_KP_Next`     | `0xff9b` | `XK_KP_Page_Down` | `0xff9b` |
| `XK_KP_End`      | `0xff9c` | `XK_KP_Begin`     | `0xff9d` |
| `XK_KP_Insert`   | `0xff9e` | `XK_KP_Delete`    | `0xff9f` |
| `XK_KP_Equal`    | `0xffbd` | `XK_KP_Multiply`  | `0xffaa` |
| `XK_KP_Add`      | `0xffab` | `XK_KP_Separator` | `0xffac` |
| `XK_KP_Subtract` | `0xffad` | `XK_KP_Decimal`   | `0xffae` |
| `XK_KP_Divide`   | `0xffaf` | `XK_KP_0`         | `0xffb0` |
| `XK_KP_1`        | `0xffb1` | `XK_KP_2`         | `0xffb2` |
| `XK_KP_3`        | `0xffb3` | `XK_KP_4`         | `0xffb4` |
| `XK_KP_5`        | `0xffb5` | `XK_KP_6`         | `0xffb6` |
| `XK_KP_7`        | `0xffb7` | `XK_KP_8`         | `0xffb8` |
| `XK_KP_9`        | `0xffb9` |                   |          |

#### Function keys (F1-F35)

| Key      | Keysym   | Key      | Keysym   |
| -------- | -------- | -------- | -------- |
| `XK_F1`  | `0xffbe` | `XK_F2`  | `0xffbf` |
| `XK_F3`  | `0xffc0` | `XK_F4`  | `0xffc1` |
| `XK_F5`  | `0xffc2` | `XK_F6`  | `0xffc3` |
| `XK_F7`  | `0xffc4` | `XK_F8`  | `0xffc5` |
| `XK_F9`  | `0xffc6` | `XK_F10` | `0xffc7` |
| `XK_F11` | `0xffc8` | `XK_L1`  | `0xffc8` |
| `XK_F12` | `0xffc9` | `XK_L2`  | `0xffc9` |
| `XK_F13` | `0xffca` | `XK_L3`  | `0xffca` |
| `XK_F14` | `0xffcb` | `XK_L4`  | `0xffcb` |
| `XK_F15` | `0xffcc` | `XK_L5`  | `0xffcc` |
| `XK_F16` | `0xffcd` | `XK_L6`  | `0xffcd` |
| `XK_F17` | `0xffce` | `XK_L7`  | `0xffce` |
| `XK_F18` | `0xffcf` | `XK_L8`  | `0xffcf` |
| `XK_F19` | `0xffd0` | `XK_L9`  | `0xffd0` |
| `XK_F20` | `0xffd1` | `XK_L10` | `0xffd1` |
| `XK_F21` | `0xffd2` | `XK_R1`  | `0xffd2` |
| `XK_F22` | `0xffd3` | `XK_R2`  | `0xffd3` |
| `XK_F23` | `0xffd4` | `XK_R3`  | `0xffd4` |
| `XK_F24` | `0xffd5` | `XK_R4`  | `0xffd5` |
| `XK_F25` | `0xffd6` | `XK_R5`  | `0xffd6` |
| `XK_F26` | `0xffd7` | `XK_R6`  | `0xffd7` |
| `XK_F27` | `0xffd8` | `XK_R7`  | `0xffd8` |
| `XK_F28` | `0xffd9` | `XK_R8`  | `0xffd9` |
| `XK_F29` | `0xffda` | `XK_R9`  | `0xffda` |
| `XK_F30` | `0xffdb` | `XK_R10` | `0xffdb` |
| `XK_F31` | `0xffdc` | `XK_R11` | `0xffdc` |
| `XK_F32` | `0xffdd` | `XK_R12` | `0xffdd` |
| `XK_F33` | `0xffde` | `XK_R13` | `0xffde` |
| `XK_F34` | `0xffdf` | `XK_R14` | `0xffdf` |
| `XK_F35` | `0xffe0` | `XK_R15` | `0xffe0` |

#### Modifier keys

| Key            | Keysym   | Key             | Keysym   |
| -------------- | -------- | --------------- | -------- |
| `XK_Shift_L`   | `0xffe1` | `XK_Shift_R`    | `0xffe2` |
| `XK_Control_L` | `0xffe3` | `XK_Control_R`  | `0xffe4` |
| `XK_Caps_Lock` | `0xffe5` | `XK_Shift_Lock` | `0xffe6` |
| `XK_Meta_L`    | `0xffe7` | `XK_Meta_R`     | `0xffe8` |
| `XK_Alt_L`     | `0xffe9` | `XK_Alt_R`      | `0xffea` |
| `XK_Super_L`   | `0xffeb` | `XK_Super_R`    | `0xffec` |
| `XK_Hyper_L`   | `0xffed` | `XK_Hyper_R`    | `0xffee` |

#### Pointer buttons

| Key                        | Keysym   | Key                      | Keysym   |
| -------------------------- | -------- | ------------------------ | -------- |
| `XK_Pointer_Left`          | `0xfee0` | `XK_Pointer_Right`       | `0xfee1` |
| `XK_Pointer_Up`            | `0xfee2` | `XK_Pointer_Down`        | `0xfee3` |
| `XK_Pointer_UpLeft`        | `0xfee4` | `XK_Pointer_UpRight`     | `0xfee5` |
| `XK_Pointer_DownLeft`      | `0xfee6` | `XK_Pointer_DownRight`   | `0xfee7` |
| `XK_Pointer_Button_Dflt`   | `0xfee8` | `XK_Pointer_Button1`     | `0xfee9` |
| `XK_Pointer_Button2`       | `0xfeea` | `XK_Pointer_Button3`     | `0xfeeb` |
| `XK_Pointer_Button4`       | `0xfeec` | `XK_Pointer_Button5`     | `0xfeed` |
| `XK_Pointer_DblClick_Dflt` | `0xfeee` | `XK_Pointer_DblClick1`   | `0xfeef` |
| `XK_Pointer_DblClick2`     | `0xfef0` | `XK_Pointer_DblClick3`   | `0xfef1` |
| `XK_Pointer_DblClick4`     | `0xfef2` | `XK_Pointer_DblClick5`   | `0xfef3` |
| `XK_Pointer_Drag_Dflt`     | `0xfef4` | `XK_Pointer_Drag1`       | `0xfef5` |
| `XK_Pointer_Drag2`         | `0xfef6` | `XK_Pointer_Drag3`       | `0xfef7` |
| `XK_Pointer_Drag4`         | `0xfef8` | `XK_Pointer_Drag5`       | `0xfefd` |
| `XK_Pointer_EnableKeys`    | `0xfef9` | `XK_Pointer_Accelerate`  | `0xfefa` |
| `XK_Pointer_DfltBtnNext`   | `0xfefb` | `XK_Pointer_DfltBtnPrev` | `0xfefc` |

#### XKB keys

| Key                              | Keysym   | Key                           | Keysym   |
| -------------------------------- | -------- | ----------------------------- | -------- |
| `XK_ISO_Lock`                    | `0xfe01` | `XK_ISO_Level2_Latch`         | `0xfe02` |
| `XK_ISO_Level3_Shift`            | `0xfe03` | `XK_ISO_Level3_Latch`         | `0xfe04` |
| `XK_ISO_Level3_Lock`             | `0xfe05` | `XK_ISO_Level5_Shift`         | `0xfe11` |
| `XK_ISO_Level5_Latch`            | `0xfe12` | `XK_ISO_Level5_Lock`          | `0xfe13` |
| `XK_ISO_Group_Shift`             | `0xff7e` | `XK_ISO_Group_Latch`          | `0xfe06` |
| `XK_ISO_Group_Lock`              | `0xfe07` | `XK_ISO_Next_Group`           | `0xfe08` |
| `XK_ISO_Next_Group_Lock`         | `0xfe09` | `XK_ISO_Prev_Group`           | `0xfe0a` |
| `XK_ISO_Prev_Group_Lock`         | `0xfe0b` | `XK_ISO_First_Group`          | `0xfe0c` |
| `XK_ISO_First_Group_Lock`        | `0xfe0d` | `XK_ISO_Last_Group`           | `0xfe0e` |
| `XK_ISO_Last_Group_Lock`         | `0xfe0f` | `XK_ISO_Left_Tab`             | `0xfe20` |
| `XK_ISO_Move_Line_Up`            | `0xfe21` | `XK_ISO_Move_Line_Down`       | `0xfe22` |
| `XK_ISO_Partial_Line_Up`         | `0xfe23` | `XK_ISO_Partial_Line_Down`    | `0xfe24` |
| `XK_ISO_Partial_Space_Left`      | `0xfe25` | `XK_ISO_Partial_Space_Right`  | `0xfe26` |
| `XK_ISO_Set_Margin_Left`         | `0xfe27` | `XK_ISO_Set_Margin_Right`     | `0xfe28` |
| `XK_ISO_Release_Margin_Left`     | `0xfe29` | `XK_ISO_Release_Margin_Right` | `0xfe2a` |
| `XK_ISO_Release_Both_Margins`    | `0xfe2b` | `XK_ISO_Fast_Cursor_Left`     | `0xfe2c` |
| `XK_ISO_Fast_Cursor_Right`       | `0xfe2d` | `XK_ISO_Fast_Cursor_Up`       | `0xfe2e` |
| `XK_ISO_Fast_Cursor_Down`        | `0xfe2f` | `XK_ISO_Continuous_Underline` | `0xfe30` |
| `XK_ISO_Discontinuous_Underline` | `0xfe31` | `XK_ISO_Emphasize`            | `0xfe32` |
| `XK_ISO_Center_Object`           | `0xfe33` | `XK_ISO_Enter`                | `0xfe34` |

#### Dead keys (accents)

| Key                        | Keysym   | Key                          | Keysym   |
| -------------------------- | -------- | ---------------------------- | -------- |
| `XK_dead_grave`            | `0xfe50` | `XK_dead_acute`              | `0xfe51` |
| `XK_dead_circumflex`       | `0xfe52` | `XK_dead_tilde`              | `0xfe53` |
| `XK_dead_perispomeni`      | `0xfe53` | `XK_dead_macron`             | `0xfe54` |
| `XK_dead_breve`            | `0xfe55` | `XK_dead_abovedot`           | `0xfe56` |
| `XK_dead_diaeresis`        | `0xfe57` | `XK_dead_abovering`          | `0xfe58` |
| `XK_dead_doubleacute`      | `0xfe59` | `XK_dead_caron`              | `0xfe5a` |
| `XK_dead_cedilla`          | `0xfe5b` | `XK_dead_ogonek`             | `0xfe5c` |
| `XK_dead_iota`             | `0xfe5d` | `XK_dead_voiced_sound`       | `0xfe5e` |
| `XK_dead_semivoiced_sound` | `0xfe5f` | `XK_dead_belowdot`           | `0xfe60` |
| `XK_dead_hook`             | `0xfe61` | `XK_dead_horn`               | `0xfe62` |
| `XK_dead_stroke`           | `0xfe63` | `XK_dead_abovecomma`         | `0xfe64` |
| `XK_dead_psili`            | `0xfe64` | `XK_dead_abovereversedcomma` | `0xfe65` |
| `XK_dead_dasia`            | `0xfe65` | `XK_dead_doublegrave`        | `0xfe66` |
| `XK_dead_belowring`        | `0xfe67` | `XK_dead_belowmacron`        | `0xfe68` |
| `XK_dead_belowcircumflex`  | `0xfe69` | `XK_dead_belowtilde`         | `0xfe6a` |
| `XK_dead_belowbreve`       | `0xfe6b` | `XK_dead_belowdiaeresis`     | `0xfe6c` |
| `XK_dead_invertedbreve`    | `0xfe6d` | `XK_dead_belowcomma`         | `0xfe6e` |
| `XK_dead_currency`         | `0xfe6f` |                              |          |

#### Dead vowels and universal entry

| Key                          | Keysym   | Key                      | Keysym   |
| ---------------------------- | -------- | ------------------------ | -------- |
| `XK_dead_a`                  | `0xfe80` | `XK_dead_A`              | `0xfe81` |
| `XK_dead_e`                  | `0xfe82` | `XK_dead_E`              | `0xfe83` |
| `XK_dead_i`                  | `0xfe84` | `XK_dead_I`              | `0xfe85` |
| `XK_dead_o`                  | `0xfe86` | `XK_dead_O`              | `0xfe87` |
| `XK_dead_u`                  | `0xfe88` | `XK_dead_U`              | `0xfe89` |
| `XK_dead_small_schwa`        | `0xfe8a` | `XK_dead_capital_schwa`  | `0xfe8b` |
| `XK_First_Virtual_Screen`    | `0xfed0` | `XK_Prev_Virtual_Screen` | `0xfed1` |
| `XK_Next_Virtual_Screen`     | `0xfed2` | `XK_Last_Virtual_Screen` | `0xfed4` |
| `XK_Terminate_Server`        | `0xfed5` | `XK_AccessX_Enable`      | `0xfe70` |
| `XK_AccessX_Feedback_Enable` | `0xfe71` | `XK_RepeatKeys_Enable`   | `0xfe72` |
| `XK_SlowKeys_Enable`         | `0xfe73` | `XK_BounceKeys_Enable`   | `0xfe74` |
| `XK_StickyKeys_Enable`       | `0xfe75` | `XK_MouseKeys_Enable`    | `0xfe76` |
| `XK_MouseKeys_Accel_Enable`  | `0xfe77` | `XK_Overlay1_Enable`     | `0xfe78` |
| `XK_Overlay2_Enable`         | `0xfe79` | `XK_AudibleBell_Enable`  | `0xfe7a` |

#### 3270 terminal keys

| Key                    | Keysym   | Key                    | Keysym   |
| ---------------------- | -------- | ---------------------- | -------- |
| `XK_3270_Duplicate`    | `0xfd01` | `XK_3270_FieldMark`    | `0xfd02` |
| `XK_3270_Right2`       | `0xfd03` | `XK_3270_Left2`        | `0xfd04` |
| `XK_3270_BackTab`      | `0xfd05` | `XK_3270_EraseEOF`     | `0xfd06` |
| `XK_3270_EraseInput`   | `0xfd07` | `XK_3270_Reset`        | `0xfd08` |
| `XK_3270_Quit`         | `0xfd09` | `XK_3270_PA1`          | `0xfd0a` |
| `XK_3270_PA2`          | `0xfd0b` | `XK_3270_PA3`          | `0xfd0c` |
| `XK_3270_Test`         | `0xfd0d` | `XK_3270_Attn`         | `0xfd0e` |
| `XK_3270_CursorBlink`  | `0xfd0f` | `XK_3270_AltCursor`    | `0xfd10` |
| `XK_3270_KeyClick`     | `0xfd11` | `XK_3270_Jump`         | `0xfd12` |
| `XK_3270_Ident`        | `0xfd13` | `XK_3270_Rule`         | `0xfd14` |
| `XK_3270_Copy`         | `0xfd15` | `XK_3270_Play`         | `0xfd16` |
| `XK_3270_Setup`        | `0xfd17` | `XK_3270_Record`       | `0xfd18` |
| `XK_3270_ChangeScreen` | `0xfd19` | `XK_3270_DeleteWord`   | `0xfd1a` |
| `XK_3270_ExSelect`     | `0xfd1b` | `XK_3270_CursorSelect` | `0xfd1c` |
| `XK_3270_PrintScreen`  | `0xfd1d` | `XK_3270_Enter`        | `0xfd1e` |

#### International composition

| Key                    | Keysym   | Key                    | Keysym   |
| ---------------------- | -------- | ---------------------- | -------- |
| `XK_Multi_key`         | `0xff20` | `XK_Codeinput`         | `0xff37` |
| `XK_SingleCandidate`   | `0xff3c` | `XK_MultipleCandidate` | `0xff3d` |
| `XK_PreviousCandidate` | `0xff3e` |                        |          |

#### Japanese keyboard support

| Key                  | Keysym   | Key                    | Keysym   |
| -------------------- | -------- | ---------------------- | -------- |
| `XK_Kanji`           | `0xff21` | `XK_Muhenkan`          | `0xff22` |
| `XK_Henkan_Mode`     | `0xff23` | `XK_Henkan`            | `0xff23` |
| `XK_Romaji`          | `0xff24` | `XK_Hiragana`          | `0xff25` |
| `XK_Katakana`        | `0xff26` | `XK_Hiragana_Katakana` | `0xff27` |
| `XK_Zenkaku`         | `0xff28` | `XK_Hankaku`           | `0xff29` |
| `XK_Zenkaku_Hankaku` | `0xff2a` | `XK_Touroku`           | `0xff2b` |
| `XK_Massyo`          | `0xff2c` | `XK_Kana_Lock`         | `0xff2d` |
| `XK_Kana_Shift`      | `0xff2e` | `XK_Eisu_Shift`        | `0xff2f` |
| `XK_Eisu_toggle`     | `0xff30` | `XK_Kanji_Bangou`      | `0xff37` |
| `XK_Zen_Koho`        | `0xff3d` | `XK_Mae_Koho`          | `0xff3e` |

#### Latin 1 (ISO-8859-1)

| Key                 | Keysym | Key                | Keysym |
| ------------------- | ------ | ------------------ | ------ |
| `XK_space`          | `0x20` | `XK_exclam`        | `0x21` |
| `XK_quotedbl`       | `0x22` | `XK_numbersign`    | `0x23` |
| `XK_dollar`         | `0x24` | `XK_percent`       | `0x25` |
| `XK_ampersand`      | `0x26` | `XK_apostrophe`    | `0x27` |
| `XK_quoteright`     | `0x27` | `XK_parenleft`     | `0x28` |
| `XK_parenright`     | `0x29` | `XK_asterisk`      | `0x2a` |
| `XK_plus`           | `0x2b` | `XK_comma`         | `0x2c` |
| `XK_minus`          | `0x2d` | `XK_period`        | `0x2e` |
| `XK_slash`          | `0x2f` | `XK_0`             | `0x30` |
| `XK_1`              | `0x31` | `XK_2`             | `0x32` |
| `XK_3`              | `0x33` | `XK_4`             | `0x34` |
| `XK_5`              | `0x35` | `XK_6`             | `0x36` |
| `XK_7`              | `0x37` | `XK_8`             | `0x38` |
| `XK_9`              | `0x39` | `XK_colon`         | `0x3a` |
| `XK_semicolon`      | `0x3b` | `XK_less`          | `0x3c` |
| `XK_equal`          | `0x3d` | `XK_greater`       | `0x3e` |
| `XK_question`       | `0x3f` | `XK_at`            | `0x40` |
| `XK_A`              | `0x41` | `XK_B`             | `0x42` |
| `XK_C`              | `0x43` | `XK_D`             | `0x44` |
| `XK_E`              | `0x45` | `XK_F`             | `0x46` |
| `XK_G`              | `0x47` | `XK_H`             | `0x48` |
| `XK_I`              | `0x49` | `XK_J`             | `0x4a` |
| `XK_K`              | `0x4b` | `XK_L`             | `0x4c` |
| `XK_M`              | `0x4d` | `XK_N`             | `0x4e` |
| `XK_O`              | `0x4f` | `XK_P`             | `0x50` |
| `XK_Q`              | `0x51` | `XK_R`             | `0x52` |
| `XK_S`              | `0x53` | `XK_T`             | `0x54` |
| `XK_U`              | `0x55` | `XK_V`             | `0x56` |
| `XK_W`              | `0x57` | `XK_X`             | `0x58` |
| `XK_Y`              | `0x59` | `XK_Z`             | `0x5a` |
| `XK_bracketleft`    | `0x5b` | `XK_backslash`     | `0x5c` |
| `XK_bracketright`   | `0x5d` | `XK_asciicircum`   | `0x5e` |
| `XK_underscore`     | `0x5f` | `XK_grave`         | `0x60` |
| `XK_quoteleft`      | `0x60` | `XK_a`             | `0x61` |
| `XK_b`              | `0x62` | `XK_c`             | `0x63` |
| `XK_d`              | `0x64` | `XK_e`             | `0x65` |
| `XK_f`              | `0x66` | `XK_g`             | `0x67` |
| `XK_h`              | `0x68` | `XK_i`             | `0x69` |
| `XK_j`              | `0x6a` | `XK_k`             | `0x6b` |
| `XK_l`              | `0x6c` | `XK_m`             | `0x6d` |
| `XK_n`              | `0x6e` | `XK_o`             | `0x6f` |
| `XK_p`              | `0x70` | `XK_q`             | `0x71` |
| `XK_r`              | `0x72` | `XK_s`             | `0x73` |
| `XK_t`              | `0x74` | `XK_u`             | `0x75` |
| `XK_v`              | `0x76` | `XK_w`             | `0x77` |
| `XK_x`              | `0x78` | `XK_y`             | `0x79` |
| `XK_z`              | `0x7a` | `XK_braceleft`     | `0x7b` |
| `XK_bar`            | `0x7c` | `XK_braceright`    | `0x7d` |
| `XK_asciitilde`     | `0x7e` | `XK_nobreakspace`  | `0xa0` |
| `XK_exclamdown`     | `0xa1` | `XK_cent`          | `0xa2` |
| `XK_sterling`       | `0xa3` | `XK_currency`      | `0xa4` |
| `XK_yen`            | `0xa5` | `XK_brokenbar`     | `0xa6` |
| `XK_section`        | `0xa7` | `XK_diaeresis`     | `0xa8` |
| `XK_copyright`      | `0xa9` | `XK_ordfeminine`   | `0xaa` |
| `XK_guillemotleft`  | `0xab` | `XK_notsign`       | `0xac` |
| `XK_hyphen`         | `0xad` | `XK_registered`    | `0xae` |
| `XK_macron`         | `0xaf` | `XK_degree`        | `0xb0` |
| `XK_plusminus`      | `0xb1` | `XK_twosuperior`   | `0xb2` |
| `XK_threesuperior`  | `0xb3` | `XK_acute`         | `0xb4` |
| `XK_mu`             | `0xb5` | `XK_paragraph`     | `0xb6` |
| `XK_periodcentered` | `0xb7` | `XK_cedilla`       | `0xb8` |
| `XK_onesuperior`    | `0xb9` | `XK_masculine`     | `0xba` |
| `XK_guillemotright` | `0xbb` | `XK_onequarter`    | `0xbc` |
| `XK_onehalf`        | `0xbd` | `XK_threequarters` | `0xbe` |
| `XK_questiondown`   | `0xbf` | `XK_Agrave`        | `0xc0` |
| `XK_Aacute`         | `0xc1` | `XK_Acircumflex`   | `0xc2` |
| `XK_Atilde`         | `0xc3` | `XK_Adiaeresis`    | `0xc4` |
| `XK_Aring`          | `0xc5` | `XK_AE`            | `0xc6` |
| `XK_Ccedilla`       | `0xc7` | `XK_Egrave`        | `0xc8` |
| `XK_Eacute`         | `0xc9` | `XK_Ecircumflex`   | `0xca` |
| `XK_Ediaeresis`     | `0xcb` | `XK_Igrave`        | `0xcc` |
| `XK_Iacute`         | `0xcd` | `XK_Icircumflex`   | `0xce` |
| `XK_Idiaeresis`     | `0xcf` | `XK_ETH`           | `0xd0` |
| `XK_Eth`            | `0xd0` | `XK_Ntilde`        | `0xd1` |
| `XK_Ograve`         | `0xd2` | `XK_Oacute`        | `0xd3` |
| `XK_Ocircumflex`    | `0xd4` | `XK_Otilde`        | `0xd5` |
| `XK_Odiaeresis`     | `0xd6` | `XK_multiply`      | `0xd7` |
| `XK_Oslash`         | `0xd8` | `XK_Ooblique`      | `0xd8` |
| `XK_Ugrave`         | `0xd9` | `XK_Uacute`        | `0xda` |
| `XK_Ucircumflex`    | `0xdb` | `XK_Udiaeresis`    | `0xdc` |
| `XK_Yacute`         | `0xdd` | `XK_THORN`         | `0xde` |
| `XK_Thorn`          | `0xde` | `XK_ssharp`        | `0xdf` |
| `XK_agrave`         | `0xe0` | `XK_aacute`        | `0xe1` |
| `XK_acircumflex`    | `0xe2` | `XK_atilde`        | `0xe3` |
| `XK_adiaeresis`     | `0xe4` | `XK_aring`         | `0xe5` |
| `XK_ae`             | `0xe6` | `XK_ccedilla`      | `0xe7` |
| `XK_egrave`         | `0xe8` | `XK_eacute`        | `0xe9` |
| `XK_ecircumflex`    | `0xea` | `XK_ediaeresis`    | `0xeb` |
| `XK_igrave`         | `0xec` | `XK_iacute`        | `0xed` |
| `XK_icircumflex`    | `0xee` | `XK_idiaeresis`    | `0xef` |
| `XK_eth`            | `0xf0` | `XK_ntilde`        | `0xf1` |
| `XK_ograve`         | `0xf2` | `XK_oacute`        | `0xf3` |
| `XK_ocircumflex`    | `0xf4` | `XK_otilde`        | `0xf5` |
| `XK_odiaeresis`     | `0xf6` | `XK_division`      | `0xf7` |
| `XK_oslash`         | `0xf8` | `XK_ooblique`      | `0xf8` |
| `XK_ugrave`         | `0xf9` | `XK_uacute`        | `0xfa` |
| `XK_ucircumflex`    | `0xfb` | `XK_udiaeresis`    | `0xfc` |
| `XK_yacute`         | `0xfd` | `XK_thorn`         | `0xfe` |
| `XK_ydiaeresis`     | `0xff` |                    |        |

#### Latin 2 (Central/Eastern Europe)

| Key               | Keysym  | Key               | Keysym  |
| ----------------- | ------- | ----------------- | ------- |
| `XK_Aogonek`      | `0x1a1` | `XK_breve`        | `0x1a2` |
| `XK_Lstroke`      | `0x1a3` | `XK_Lcaron`       | `0x1a5` |
| `XK_Sacute`       | `0x1a6` | `XK_Scaron`       | `0x1a9` |
| `XK_Scedilla`     | `0x1aa` | `XK_Tcaron`       | `0x1ab` |
| `XK_Zacute`       | `0x1ac` | `XK_Zcaron`       | `0x1ae` |
| `XK_Zabovedot`    | `0x1af` | `XK_aogonek`      | `0x1b1` |
| `XK_ogonek`       | `0x1b2` | `XK_lstroke`      | `0x1b3` |
| `XK_lcaron`       | `0x1b5` | `XK_sacute`       | `0x1b6` |
| `XK_caron`        | `0x1b7` | `XK_scaron`       | `0x1b9` |
| `XK_scedilla`     | `0x1ba` | `XK_tcaron`       | `0x1bb` |
| `XK_zacute`       | `0x1bc` | `XK_doubleacute`  | `0x1bd` |
| `XK_zcaron`       | `0x1be` | `XK_zabovedot`    | `0x1bf` |
| `XK_Racute`       | `0x1c0` | `XK_Abreve`       | `0x1c3` |
| `XK_Lacute`       | `0x1c5` | `XK_Cacute`       | `0x1c6` |
| `XK_Ccaron`       | `0x1c8` | `XK_Eogonek`      | `0x1ca` |
| `XK_Ecaron`       | `0x1cc` | `XK_Dcaron`       | `0x1cf` |
| `XK_Dstroke`      | `0x1d0` | `XK_Nacute`       | `0x1d1` |
| `XK_Ncaron`       | `0x1d2` | `XK_Odoubleacute` | `0x1d5` |
| `XK_Rcaron`       | `0x1d8` | `XK_Uring`        | `0x1d9` |
| `XK_Udoubleacute` | `0x1db` | `XK_Tcedilla`     | `0x1de` |
| `XK_racute`       | `0x1e0` | `XK_abreve`       | `0x1e3` |
| `XK_lacute`       | `0x1e5` | `XK_cacute`       | `0x1e6` |
| `XK_ccaron`       | `0x1e8` | `XK_eogonek`      | `0x1ea` |
| `XK_ecaron`       | `0x1ec` | `XK_dcaron`       | `0x1ef` |
| `XK_dstroke`      | `0x1f0` | `XK_nacute`       | `0x1f1` |
| `XK_ncaron`       | `0x1f2` | `XK_odoubleacute` | `0x1f5` |
| `XK_rcaron`       | `0x1f8` | `XK_uring`        | `0x1f9` |
| `XK_udoubleacute` | `0x1fb` | `XK_tcedilla`     | `0x1fe` |
| `XK_abovedot`     | `0x1ff` |                   |         |

#### Latin 3 (South Europe)

| Key              | Keysym  | Key              | Keysym  |
| ---------------- | ------- | ---------------- | ------- |
| `XK_Hstroke`     | `0x2a1` | `XK_Hcircumflex` | `0x2a6` |
| `XK_Iabovedot`   | `0x2a9` | `XK_Gbreve`      | `0x2ab` |
| `XK_Jcircumflex` | `0x2ac` | `XK_hstroke`     | `0x2b1` |
| `XK_hcircumflex` | `0x2b6` | `XK_idotless`    | `0x2b9` |
| `XK_gbreve`      | `0x2bb` | `XK_jcircumflex` | `0x2bc` |
| `XK_Cabovedot`   | `0x2c5` | `XK_Ccircumflex` | `0x2c6` |
| `XK_Gabovedot`   | `0x2d5` | `XK_Gcircumflex` | `0x2d8` |
| `XK_Ubreve`      | `0x2dd` | `XK_Scircumflex` | `0x2de` |
| `XK_cabovedot`   | `0x2e5` | `XK_ccircumflex` | `0x2e6` |
| `XK_gabovedot`   | `0x2f5` | `XK_gcircumflex` | `0x2f8` |
| `XK_ubreve`      | `0x2fd` | `XK_scircumflex` | `0x2fe` |

#### Latin 4 (Baltic/Nordic)

| Key            | Keysym  | Key          | Keysym  |
| -------------- | ------- | ------------ | ------- |
| `XK_kra`       | `0x3a2` | `XK_kappa`   | `0x3a2` |
| `XK_Rcedilla`  | `0x3a3` | `XK_Itilde`  | `0x3a5` |
| `XK_Lcedilla`  | `0x3a6` | `XK_Emacron` | `0x3aa` |
| `XK_Gcedilla`  | `0x3ab` | `XK_Tslash`  | `0x3ac` |
| `XK_rcedilla`  | `0x3b3` | `XK_itilde`  | `0x3b5` |
| `XK_lcedilla`  | `0x3b6` | `XK_emacron` | `0x3ba` |
| `XK_gcedilla`  | `0x3bb` | `XK_tslash`  | `0x3bc` |
| `XK_ENG`       | `0x3bd` | `XK_eng`     | `0x3bf` |
| `XK_Amacron`   | `0x3c0` | `XK_Iogonek` | `0x3c7` |
| `XK_Eabovedot` | `0x3cc` | `XK_Imacron` | `0x3cf` |
| `XK_Ncedilla`  | `0x3d1` | `XK_Omacron` | `0x3d2` |
| `XK_Kcedilla`  | `0x3d3` | `XK_Uogonek` | `0x3d9` |
| `XK_Utilde`    | `0x3dd` | `XK_Umacron` | `0x3de` |
| `XK_amacron`   | `0x3e0` | `XK_iogonek` | `0x3e7` |
| `XK_eabovedot` | `0x3ec` | `XK_imacron` | `0x3ef` |
| `XK_ncedilla`  | `0x3f1` | `XK_omacron` | `0x3f2` |
| `XK_kcedilla`  | `0x3f3` | `XK_uogonek` | `0x3f9` |
| `XK_utilde`    | `0x3fd` | `XK_umacron` | `0x3fe` |

#### Latin 8 (Romanian)

| Key              | Keysym      | Key              | Keysym      |
| ---------------- | ----------- | ---------------- | ----------- |
| `XK_Wcircumflex` | `0x1000174` | `XK_wcircumflex` | `0x1000175` |
| `XK_Ycircumflex` | `0x1000176` | `XK_ycircumflex` | `0x1000177` |
| `XK_Babovedot`   | `0x1001e02` | `XK_babovedot`   | `0x1001e03` |
| `XK_Dabovedot`   | `0x1001e0a` | `XK_dabovedot`   | `0x1001e0b` |
| `XK_Fabovedot`   | `0x1001e1e` | `XK_fabovedot`   | `0x1001e1f` |
| `XK_Mabovedot`   | `0x1001e40` | `XK_mabovedot`   | `0x1001e41` |
| `XK_Pabovedot`   | `0x1001e56` | `XK_pabovedot`   | `0x1001e57` |
| `XK_Sabovedot`   | `0x1001e60` | `XK_sabovedot`   | `0x1001e61` |
| `XK_Tabovedot`   | `0x1001e6a` | `XK_tabovedot`   | `0x1001e6b` |
| `XK_Wgrave`      | `0x1001e80` | `XK_wgrave`      | `0x1001e81` |
| `XK_Wacute`      | `0x1001e82` | `XK_wacute`      | `0x1001e83` |
| `XK_Wdiaeresis`  | `0x1001e84` | `XK_wdiaeresis`  | `0x1001e85` |
| `XK_Ygrave`      | `0x1001ef2` | `XK_ygrave`      | `0x1001ef3` |

#### Latin 9 (Euro and Ij ligature)

| Key             | Keysym   | Key     | Keysym   |
| --------------- | -------- | ------- | -------- |
| `XK_OE`         | `0x13bc` | `XK_oe` | `0x13bd` |
| `XK_Ydiaeresis` | `0x13be` |         |          |

## Appendix C: Glossary

| Term                        | Meaning                                                                                                          |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Alpha channel               | The fourth byte of a color: how opaque the pixel is (0 transparent, 255 solid)                                   |
| Backend                     | The piece of MiniLibX that talks to one specific graphics system (XCB, Wayland, AppKit)                          |
| Blit                        | Copying a whole image onto the window in one operation (`mlx_put_image_to_window`)                               |
| bpp (bits per pixel)        | How many bits one pixel occupies; 32 bpp = 4 bytes per pixel                                                     |
| Callback                    | A function you register; MiniLibX calls it when an event happens                                                 |
| Compositor                  | The program that puts all windows together on screen (used by Wayland)                                           |
| Delta time                  | The time between two frames; you measure it to make motion speed constant                                        |
| Double buffering            | Drawing in a private buffer and showing it only when complete, to avoid flicker                                  |
| Event loop                  | The endless cycle that waits for events and dispatches them to your callbacks                                    |
| Expose                      | An event meaning "a part of your window needs to be redrawn" (all backends, once after the window first appears) |
| Framebuffer                 | A region of memory holding one pixel value per screen position; here, an MLX image                               |
| Hook                        | Another name for registering a callback                                                                          |
| Keycode                     | The physical identity of a key on the keyboard (hardware dependent)                                              |
| Keysym                      | The logical meaning of a key, X11 style (`a` = 97, Escape = 65307)                                               |
| mlx_ptr / win_ptr / img_ptr | Identifiers: connection / window / image; opaque integers you pass back to MiniLibX                              |
| Stride                      | Bytes per row in a buffer, padding included; `size_line` in the wrapper                                          |
| Wheel                       | A `.whl` file: the package format used to install the mlx Python library                                         |
| XCB / Wayland / AppKit      | The three backends MiniLibX supports: Linux X11, Linux Wayland, macOS                                            |
