# Zhusk:

*ZHusk, a library to streamline workflows and assist those who work extensively with the terminal and more.*

## Version:

**Zhusk Version:** *0.1.4*

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

*To assist the 'termios' library.*

### time

*For animated typing functions.*

### platform

*To determine which operating system it is.*

### subprocess

*To run commands such as IP discovery.*

### termios

*It is only imported if the system is macOS/Linux and the user employs a function that requires it.*

### signal

*For enable/disable keyboard interrupt.*

## Functions:

### block()

*This turns off terminal 'ECHO', preventing the terminal from immediately displaying what is typed—everything goes into the keyboard buffer instead; unless used in conjunction with the 'ignore' function, everything previously typed will appear as soon as 'unblock' is used.*

*Only MacOS and Linux.*

**Usage example:**

```
import zhusk

zhusk.block()

print("Hello world")
```

### unblock()

*Typically used when you want to use an 'input()' function; you can also use 'input_slow(support=True)'—simply include a 'block()' at the beginning of the code, and you won't need to worry about it.*

*Only MacOS and Linux.*

**Usage example:**

```
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

*This clears the user's keyboard buffer, ensuring that multiple characters that had not appeared due to the 'block' function are not displayed upon receiving new 'input'.*

*Only MacOS and Linux.*

**Usage example:**

```
import zhusk

zhusk.block()

print("Hello world")
zhusk.ignore()
zhusk.unblock() # Basically, following this logic, if the user jumped onto the keyboard, your program and the input would still appear in an organized way.
input("Your name: ")
```

### clear()

*Clears the terminal, quickly and simply.*

*Windows, MacOS and Linux.*

**Usage example:**

```
import zhusk

zhusk.clear() # If the guy's terminal was dirty, this would have cleaned it.
print("Hello world")
```

### off_interrupt()

*This disables the 'keyboard interrupt' capability, preventing 'Ctrl + C' from interrupting the code currently running in the terminal.*

*Windows, MacOS and Linux.*

**Usage example:**

```
import zhusk

zhusk.off_interrupt()
```

### on_interrupt()

*This reverses the action of the 'off_interrupt' function.*

*Windows, MacOS and Linux.*

**Usage example:**

```
import zhusk

zhusk.off_interrupt() # CTRL + C disabled.

zhusk.on_interrupt() # CTRL + C enabled.
```

### validate_ip()

*Checks if an IPv4 or IPv6 is valid; returns 'True' or 'False'.*

*Windows, MacOS and Linux.*

**Usage example:**

```
import zhusk

print("Hello world")
ip = input("Enter your IP: ")
check_ip = zhusk.validate_ip(ip)
print(f"Your IP is: {check_ip}") # False/True.
```

### validate_email()

*Email validation based on RFC 5322 documentation; it returns 'True' or 'False' based on the email's validity.*

*Windows, MacOS and Linux.*

**Usage example:**

```
import zhusk

print("Hello world")
email = input("Enter your e-mail: ")
check_email = zhusk.validate_email(email)
print(f"Your e-mail is: {check_email}") # False/True.
```

### my_ip()

*Shows your public IPV4 or IPV6.*

*Windows, MacOS and Linux.*

**Usage example:**

```
import zhusk

print("Hello world")
print(f"Your IPV4 is: {zhusk.my_ip()}") # Shows IPV4.
```

### print_slow()

*It displays text letter by letter in an animated fashion, creating a typing effect that you will likely want to use throughout the entire system.*

*Windows, MacOS and Linux.*

**Usage example:**

```
import zhusk

zhusk.print_slow("Hello world")
zhusk.print_slow("Hello world", temp=0.01) # The default 'temp' is 0.02, but you can change it.
```

### input_slow()

*It displays text letter by letter in an animated fashion, creating a typing effect; and at the end, it returns an 'input()'.*

*Windows, MacOS and Linux.*

**Usage example:**

```
import zhusk

zhusk.input_slow("Your name: ")
zhusk.input_slow("Your country: ", temp=0.01) # The default 'temp' is 0.02, but you can change it too.
```

## General Example (Windows, MacOS, Linux):

```
import zhusk

zhusk.clear() # Clears terminal.

zhusk.print_slow("\nHello user, this is a security system")
name = zhusk.input_slow("\nType your name: ")
zhusk.print_slow(f"\nSure, {name}.\nYour public IPV4 is: {zhusk.my_ip()}\nYour public IPV6 is: {zhusk.my_ip(ipv4=False, ipv6=True)}")
```

## General Example (MacOS, Linux):

```
import zhusk

zhusk.block() # Now the user cannot clutter the terminal while your program is running.
zhusk.clear() # Clears terminal.

zhusk.print_slow("\nHello user, this is a security system.")
name = zhusk.input_slow("\nType your name: ", support=True) # Set support to True so the code releases the block(), and reapplies it once the input finishes — that simple.
zhusk.print_slow(f"\nSure, {name}.\nYour public IPV4 is: {zhusk.my_ip()}\nYour public IPV6 is: {zhusk.my_ip(ipv4=False, ipv6=True)}")
```

## Error Handling:

*ZHusk only raises errors of type 'ZhuskError'; the recommended approach is to read the error message and act accordingly, but if you'd rather ignore it, you can do so as follows:*

```
import zhusk

try:
    zhusk.my_ip(ipv4=True, ipv6=True) # This triggers ZhuskError; it can only receive IPV4 or IPV6, not both.
except zhusk.ZhuskError:
    pass
```

## License and Author:

*This project is licensed under the MIT License. See the LICENSE file for details.*

*Zhusk Project - By FloppzH*

## Support:

**Discord Contact:** floppzh

*If you have any problems, questions, suggestions, or anything else, feel free to get in touch.*

## Links:

PyPI: <https://pypi.org/project/zhusk/>
