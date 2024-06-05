# vSerial-Python
Vescent's official serial wrapper for interfacing with Vescent products via Python, with usage examples.

## About
*vSerial* is a fast, cross platform, general purpose Python library that implements the basic functions needed to begin programmatically interfacing with Vescent SLICE and FFC products.

## Installation and Usage
1. Download vSerial.py and place it in your Python project folder.
2. In your own Python file, import vCommHandler
3. Create a local vCommHandler object and open the appropriate Serial Port using the **open()** command.
4. Use the **query()** function to send a command to the device and return its response as soon as it's received.
	- vCommHandler also provides the **send()** and **read()** commands for more low-level control.  In nearly all circumstances, **query()** is the only command you will need to use.

## Dependencies
### pySerial
*vSerial* is a convenience wrapper for pySerial by Chris Liechti, so you must install pySerial first before using *vSerial*.
If your Python environment has pip, you can install pySerial with the following command:
```
pip install pyserial
```
#### pySerial Project Links
- https://github.com/pyserial/pyserial
- https://pypi.org/project/pyserial/
- https://pyserial.readthedocs.io/en/latest/pyserial.html
	
## Compatibility
*vSerial* is written for Python 3.  Python 2.7 is unsupported.

Thanks to pySerial's cross-platform compatibility, vSerial should work on Windows, OSX, Linux, and BSD systems (although we've only tested it on Windows and Linux).

**Note:** While *vSerial* itself is written to be OS-agnostic, some of the examples may contain Windows-specific code, such as utilizing COM ports instead of generic Serial port handles.

## Regarding Support
*vSerial* is distributed in the hope that it will be useful, but is not an officially-released Vescent product.  Technical support for this library will not be provided, and no guarantee of functionality is made.  See the License section below.

## License
MIT License

Copyright (c) 2024 Vescent Technologies, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

