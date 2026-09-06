# Zhusk:

_ZHusk, a library to streamline workflows and assist those who work extensively with the terminal and more._

## Version:

**Zhusk Version:** _0.1.1_

## Installation:

```
pip install zhusk
```

## To Update:

```
pip install --upgrade --force-reinstall zhusk
```

## Requirements:

**Minimum Python version required:** 3.8

**Minimum Python version tested:** 3.12.3

## Libraries Used:

### sys

_To assist the 'termios' library._

### time

_For animated typing functions._

### platform

_To determine which operating system it is._

### subprocess

_To run commands such as IP discovery._

### termios

_It is only imported if the system is macOS/Linux and the user employs a function that requires it._

## Functions:

### block()

_This turns off terminal 'ECHO', preventing the terminal from immediately displaying what is typed—everything goes into the keyboard buffer instead; unless used in conjunction with the 'ignore' function, everything previously typed will appear as soon as 'unblock' is used._

_Only MacOS and Linux._

**Usage example:**

```python
import zhusk

zhusk.block()

print("Hello world")
```

### unblock()

*Typically used when you want to use an 'input()' function; you can also use 'input_slow(support=True)'—simply include a 'block()' at the beginning of the code, and you won't need to worry about it.*

_Only MacOS and Linux._

**Usage example:**

```python
import zhusk
import time

zhusk.block()

print("Hello world")
time.sleep(2) # If you try to type during this time, nothing will happen (if 'block' weren't called, the terminal would end up very messy).

zhusk.unblock()
zhusk.input_slow("Your name: ") # Since 'support=True' was not used, you had to handle the top and bottom lines manually. Apart from that, without using 'ignore()', everything the user typed during those 2 seconds will appear here.
zhusk.block()
```

### ignore()

_This clears the user's keyboard buffer, ensuring that multiple characters that had not appeared due to the 'block' function are not displayed upon receiving new 'input'._

_Only MacOS and Linux._

**Usage example:**

```python
import zhusk

zhusk.block()

print("Hello world")
zhusk.ignore()
zhusk.unblock() # Basically, following this logic, if the user jumped onto the keyboard, your program and the input would still appear in an organized way.
input("Your name: ")
```

### clear()

_Clears the terminal, quickly and simply._

_Windows, MacOS and Linux._

**Usage example:**

```python
import zhusk

zhusk.clear() # If the guy's terminal was dirty, this would have cleaned it.
print("Hello world")
```

### my_ip()

_Shows your public IPV4 or IPV6._

_Windows, MacOS and Linux._

**Usage example:**

```python
import zhusk

print("My cyber program")
print(f"Your IPV4 is: {zhusk.my_ip()}") # Shows IPV4.
```

### print_slow()

_It displays text letter by letter in an animated fashion, creating a typing effect that you will likely want to use throughout the entire system._

_Windows, MacOS and Linux._

**Usage example:**

```python
import zhusk

zhusk.print_slow("Hello world")
zhusk.print_slow("Hello world", temp=0.01) # The default 'temp' is 0.02, but you can change it.
```

### input_slow()

_It displays text letter by letter in an animated fashion, creating a typing effect; and at the end, it returns an 'input()'._

_Windows, MacOS and Linux._

**Usage example:**

```python
import zhusk

zhusk.input_slow("Your name: ")
zhusk.input_slow("Your country: ", temp=0.01) # The default 'temp' is 0.02, but you can change it too.
```

## General Example (Windows, MacOS, Linux):

```python
import zhusk

zhusk.clear() # Clears terminal.

zhusk.print_slow("\nHello user, this is a security system")
name = zhusk.input_slow("\nType your name: ")
zhusk.print_slow(f"\nSure, {name}.\nYour public IPV4 is: {zhusk.my_ip()}\nYour public IPV6 is: {zhusk.my_ip(ipv4=False, ipv6=True)}")
```

## General Example (MacOS, Linux):

```python
import zhusk

zhusk.block() # Now the user cannot clutter the terminal while your program is running.
zhusk.clear() # Clears terminal.

zhusk.print_slow("\nHello user, this is a security system.")
name = zhusk.input_slow("\nType your name: ", support=True) # Set support to True so the code releases the block(), and reapplies it once the input finishes — that simple.
zhusk.print_slow(f"\nSure, {name}.\nYour public IPV4 is: {zhusk.my_ip()}\nYour public IPV6 is: {zhusk.my_ip(ipv4=False, ipv6=True)}")
```

## Error Handling:

_ZHusk only raises errors of type 'ZhuskError'; the recommended approach is to read the error message and act accordingly, but if you'd rather ignore it, you can do so as follows:_

```python
import zhusk

try:
    zhusk.my_ip(ipv4=True, ipv6=True) # This triggers ZhuskError; it can only receive IPV4 or IPV6, not both.
except zhusk.ZhuskError:
    pass
```

## License and Author:

_This project is licensed under the MIT License. See the LICENSE file for details._

_Zhusk Project - By FloppzH_

## Support:

**Discord Contact:** floppzh

_If you have any problems, questions, suggestions, or anything else, feel free to get in touch._

## Links:

**Repository:** https://pypi.org/project/zhusk/0.1.0/
