from .libraries import *



# Support for Linux/Unix terminals:



Started_support = False
Supported = None


def _checking():
    if SO in ("Linux", "Darwin"): # 'SO' is defined in 'libraries.py'.
        try:
            global termios
            import termios
            return True
        except ImportError:
            raise ZhuskError("\nThe 'termios' library is not installed; for what you want to do, this will only work if you install it.\n")
        
    else:
        return False


def _check():
    global Started_support
    Started_support = True
    return _checking()


def _warning():
    global Started_support, Supported
    if not Started_support:
        Supported = _check()

    if not Supported:
        raise ZhuskError("\nYou are not on a platform that supports this function (probably the 'block', 'unblock', or 'ignore' functions); the function being called uses the 'termios' library, which is exclusive to Linux/Unix systems.\n")


def _block_configs():
    fd = sys.stdin.fileno()
    new = termios.tcgetattr(fd)
    return fd, new


def block() -> None:
    """This turns off terminal 'ECHO', preventing the terminal from immediately displaying what is typed—everything goes into the keyboard buffer instead; unless used in conjunction with the 'ignore' function, everything previously typed will appear as soon as 'unblock' is used.

    Returns:
        None: This function does not return anything.

    Example:
        >>> block()
    """

    _warning()
    fd, new = _block_configs()
    new[3] &= ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, new)


def unblock() -> None:
    """Typically used when you want to use an 'input()' function; you can also use 'input_slow(support=True)'—simply include a 'block()' at the beginning of the code, and you won't need to worry about it.

    Returns:
        None: This function does not return anything.

    Example:
        >>> unblock()
    """

    _warning()
    fd, new = _block_configs()
    new[3] |= termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, new)


def ignore() -> None:
    """This clears the users keyboard buffer, ensuring that multiple characters that had not appeared due to the 'block' function are not displayed upon receiving new 'input'.

    Returns:
        None: This function does not return anything.

    Example:
        >>> ignore()
    """

    _warning()
    termios.tcflush(sys.stdin, termios.TCIFLUSH)



# Quick commands:



def clear() -> None:
    """This sends a 'clear' command to the terminal—simple.

    Returns:
        None: This function does not return anything.

    Example:
        >>> clear()
    """

    if SO in ("Linux", "Darwin"): # 'SO' is defined in 'libraries.py'
        subprocess.run("clear", shell=True)

    else:
        subprocess.run("cls", shell=True)


def my_ip(ipv4: bool = True, ipv6: bool = False, return_str_error: bool = True, return_zhusk_error: bool = False):
    """Shows your IPv4 or IPv6 address.

    Args:
        ipv4 (bool): Specify whether you want IPv4; 'True' by default.
        ipv6 (bool): Specify whether you want IPv6; 'False' by default.
        return_str_error (bool): 'True' by default; if you do not want to receive errors in str format, set it to 'False'.
        return_zhusk_error (bool): 'False' by default; if you want to stop the code execution in case the IP is not collected, set it to 'True'.

    Returns:
        str: The default behavior is to return the collected IP as a string, or an error message if it cannot be collected.
        int: If 'return_str_error' is set to 'False', any error in the collections returns 1.
    
    Raises:
        ZhuskError: It may trigger if you set 'ipv4' and 'ipv6' to 'True', and it can also optionally trigger in cases of collection errors—simply enable 'return_zhusk_error = True'.

    Note:
        In the future, the software will also be able to return IPs in 'int' format (optional and disabled by default).

    Example:
        >>> ip = my_ip(ipv4 = True)
        >>> print(ip)
        142.250.190.78
    """

    if ipv4 and ipv6:
        raise ZhuskError("\nYou cannot use the 'my_ip' function with both IPv4 and IPv6 set to 'True'; if you want two results, call the function twice.\n")

    elif ipv4:
        ip = subprocess.run("curl -4 ifconfig.me", shell=True, capture_output=True, text=True)

        if return_zhusk_error and ip.returncode != 0:
            raise ZhuskError("\nError collecting the IPV4\n")

        elif return_str_error and ip.returncode != 0:
            return "Error collecting the IPV4"
        
        elif ip.returncode != 0:
            return 1

        else:
            return ip.stdout

    elif ipv6:
        ip = subprocess.run("curl -6 ifconfig.me", shell=True, capture_output=True, text=True)

        if return_zhusk_error and ip.returncode != 0:
            raise ZhuskError("\nError collecting the IPV6\n")

        elif return_str_error and ip.returncode != 0:
            return "Error collecting the IPV6"
        
        elif ip.returncode != 0:
            return 1

        else:
            return ip.stdout



# Customizations:



def print_slow(text: str, temp: float = 0.02) -> None:
    """Prints text to the screen, letter by letter, with a typing effect.

    Args:
        text (str): The text that will be displayed.
        temp (float, optional): Wait time between each character, in seconds. Default is 0.02.

    Returns:
        None: This function does not return anything.

    Example:
        >>> print_slow("Hello world")
        Hello world
    """

    for letter in text:
        print(letter, end="", flush=True)
        time.sleep(temp)
    print()
    return


def input_slow(text: str, temp: float = 0.02, support: bool = False) -> str:
    """Prints text to the screen, letter by letter, with a typing effect; and at the end, it releases an input.
    
    Args:
        text (str): The text that will be displayed.
        temp (float, optional): Wait time between each character, in seconds. Default is 0.02.
        support (bool, optional): Along with the 'block()' at the beginning of the code, this will be useful for making the terminal unpolluted for Linux/macOS users.

    Returns:
        str: This function returns a STR, it is 'input()'.

    Example:
        >>> input_slow("Your name: ")
        Your name: 
    """

    for letter in text:
        print(letter, end="", flush=True)
        time.sleep(temp)

    if support:
        ignore()
        unblock()

    inputer = input()

    if support:
        block()

    return inputer
