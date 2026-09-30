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
        >>> zhusk.block()
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
        >>> zhusk.unblock()
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
        >>> zhusk.ignore()
    """

    _warning()
    termios.tcflush(sys.stdin, termios.TCIFLUSH)



# Quick commands:



def clear() -> None:
    """This sends a 'clear' command to the terminal—simple.

    Returns:
        None: This function does not return anything.

    Example:
        >>> zhusk.clear()
    """

    if SO in ("Linux", "Darwin"): # 'SO' is defined in 'libraries.py'.
        subprocess.run("clear", shell=True)

    else:
        subprocess.run("cls", shell=True)


def off_interrupt() -> None:
    """This disables the 'keyboard interrupt' capability, preventing 'Ctrl + C' from interrupting the code currently running in the terminal.

    Returns:
        None: This function does not return anything.

    Example:
        >>> zhusk.off_interrupt()
    """

    signal.signal(signal.SIGINT, signal.SIG_IGN)


def on_interrupt() -> None:
    """This turns back on what you turned off ('keyboard interrupt').

    Returns:
        None: This function does not return anything.

    Example:
        >>> zhusk.on_interrupt()
    """

    signal.signal(signal.SIGINT, signal.SIG_DFL)



# Validations and Data:



def validate_ip(ip: str, ipv4: bool = True, ipv6: bool = False, realist: bool = True) -> bool:
    """IP address validation. Checks if the entered IP has a valid format; you can choose whether to validate for IPv4 or IPv6.

    Args:
        ip (str): The basis for validation, required in str format.
        ipv4 (bool): Checks if the IPv4 address format is valid; 'True' by default.
        ipv6 (bool): Checks if the IPv6 address format is valid; 'False' by default.
        realist (bool): When this is set to 'True', the function will return some potential IPs as 'False' because they are unrealistic in the real world (the mathematical probability of their existence is zero); when set to 'False', the function operates based on mathematical logic, allowing for many IPs that do not exist but are mathematically possible.

    Returns:
        bool: Returns 'True' or 'False'.
    
    Raises:
        ZhuskError: It may trigger if you set 'ipv4' and 'ipv6' to 'True' or if you don't pass an 'ip' parameter in str format.

    Example:
        >>> testing_ip = zhusk.validate_ip("127.0.0.1")
        >>> print(testing_ip)
        True
    """

    if ipv4 and ipv6:
        raise ZhuskError("\nYou cannot use the 'validate_ip' function with both IPv4 and IPv6 set to 'True'; if you want two results, call the function twice.\n")

    elif not ipv4 and not ipv6:
        raise ZhuskError("\nIt is necessary to define how the IP will be treated ('ipv4' or 'ipv6').\n")

    elif not isinstance(ip, str):
        raise ZhuskError("\nThis function only accepts the 'ip' parameter as a string.\n")

    elif ipv4:
        points = ip.count(".")
        divisions = ip.split(".")
        integer = ip.replace(".", "")

        try:
            int(integer)
        except ValueError:
            raise ZhuskError("\nValueError: In the 'validate_ip' function, you can only use numbers and dots in the IP parameter.\n")

        if not points == 3:
            return False

        elif any(cond == "" for cond in divisions):
            return False

        elif any(int(cond) > 255 or int(cond) < 0 for cond in divisions):
            return False

        else:
            return True

    elif ipv6:
        points = ip.count(":")
        double_points = ip.count("::")
        divisions = ip.split(":")
        replaced = ip.replace(":", "")
        AF09 = ("a", "b", "c", "d", "e", "f", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9")

        for thing in replaced:
            if not thing.lower() in AF09:
                return False

        if len(replaced) > 32:
            return False

        elif replaced.isalpha() or replaced == "":
            if realist:
                return False # Mathematically impossible nowadays/Unrealistic.

        elif points < 2 or points > 7 or double_points > 1:
            return False

        elif double_points:
            index = divisions.index("")
            while len(divisions) < 8:
                divisions.insert(index, "0000")
            replaced = "".join(divisions)

            if len(replaced) < 8:
                return False

        elif len(replaced) < 8: # I couldn't find a good place to put just a single check without turning all the 'elif's into 'if's.
            return False

        for thing in divisions:
            if len(thing) > 4:
                return False

        return True


def validate_email(email: str, realist: bool = True) -> bool:
    """Email validation based on RFC 5322 documentation; it returns 'True' or 'False' based on the email's validity. It aims for realism, so it may return 'False' for some theoretically valid emails; if you prefer mathematical logic over modern-day realism, set the 'realist' parameter to 'False'.

    Args:
        email (str): The email that will be validated, required in str format.
        realist (bool): This alters the validation method; if set to 'True', some theoretically valid emails may return 'False'. The realistic approach attempts to determine whether an email "makes sense," rather than verifying if it is 100% valid. If you prefer strict logic, set the 'realist' parameter to 'False'.

    Returns:
        bool: Returns 'True' or 'False'.
    
    Raises:
        ZhuskError: This occurs if the 'email' parameter is not provided as a string value.

    Example:
        >>> testing_email = zhusk.validate_email("SlavaRussia@gmail.com")
        >>> testing_email_2 = zhusk.validate_email("SlavaIsrael..@gmail.com")
        >>> print(testing_email, testing_email_2)
        True False 
    """

    if not isinstance(email, str):
        raise ZhuskError("\nThis function only accepts the 'email' parameter as a string.\n")

    try:
        ats = email.count("@")
        points = email.count(".")
        double_points = email.count("..")
        division = email.split("@")
        start_email = len(division[0])
        end_email = len(division[1])
        before_end = ""
    except Exception:
        return False

    permitted_before_end = (
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
        )

    before_at = (
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        ".", "!", "#", "$", "%", "&", "'", "*", "+", "-", "/", "=", "?",
        "^", "_", "`", "{", "|", "}", "~"
    )

    after_at = (
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        ".", "-"
    )

    prohibited = (
        ".", "!", "#", "$", "%", "&", "'", "*", "+", "-", "/", "=", "?",
        "^", "_", "`", "{", "|", "}", "~"
    )

    if len(email) > 150:
        if realist:
            return False

        elif len(email) > 255:
            return False

    elif not ats == 1:
        return False

    elif double_points:
        return False

    elif points > 12:
        if realist:
            return False

        elif points > 158:
            return False

    elif start_email > 63 or start_email + end_email > 254:
        return False

    elif start_email < 4 or end_email < 6:
        if realist:
            return False

        elif start_email < 1 or end_email < 4:
            return False

    elif division[0].startswith(prohibited) or division[0].endswith(prohibited):
        return False

    elif division[1].startswith(prohibited) or division[1].endswith(prohibited):
        return False

    elif any(current_character == next_character and current_character in prohibited for current_character, next_character in zip(division[1], division[1][1:])):
        return False

    elif any(current_character == "." and other_character in prohibited for current_character, other_character in zip(division[1], division[1][1:])):
        return False

    elif any(current_character in prohibited and other_character == "." for current_character, other_character in zip(division[1], division[1][1:])):
        return False

    for thing in email[::-1]:
        if thing == ".":
            if len(before_end) < 2:
                return False

            break

        elif thing == "@":
            return False

        else:
            before_end += thing

    for thing in before_end:
        if not thing.lower() in permitted_before_end:
            return False

    for thing in division[0]:
        if not thing.lower() in before_at:
            return False

    for thing in division[1]:
        if not thing.lower() in after_at:
            return False

    return True


def my_ip(ipv4: bool = True, ipv6: bool = False, return_str_error: bool = True, return_zhusk_error: bool = False): # -> Possible different returns.
    """Shows your IPv4 or IPv6 address.

    Args:
        ipv4 (bool): Specify whether you want IPv4; 'True' by default.
        ipv6 (bool): Specify whether you want IPv6; 'False' by default.
        return_str_error (bool, optional): 'True' by default; if you do not want to receive errors in str format, set it to 'False'.
        return_zhusk_error (bool, optional): 'False' by default; if you want to stop the code execution in case the IP is not collected, set it to 'True'.

    Returns:
        str: The default behavior is to return the collected IP as a string, or an error message if it cannot be collected.
        int: If 'return_str_error' is set to 'False', any error in the collections returns 1.

    Raises:
        ZhuskError: It may trigger if you set 'ipv4' and 'ipv6' to 'True', and it can also optionally trigger in cases of collection errors—simply enable 'return_zhusk_error = True'.

    Note:
        VPNs like Proton block IPv6 results, causing a timeout; the same can happen with other VPNs that do not route IPv6 traffic.
        In the future, the software will also be able to return IPs in 'int' format (optional and disabled by default).

    Example:
        >>> ip = zhusk.my_ip(ipv4 = True)
        >>> print(ip)
        142.250.190.78
    """

    if ipv4 and ipv6:
        raise ZhuskError("\nYou cannot use the 'my_ip' function with both IPv4 and IPv6 set to 'True'; if you want two results, call the function twice.\n")

    elif ipv4:
        try:
            ip = subprocess.run("curl -4 ifconfig.me", shell=True, capture_output=True, text=True, timeout=5)
        except subprocess.TimeoutExpired:
            ip.returncode = 0

        if return_zhusk_error and ip.returncode != 0:
            raise ZhuskError("\nError collecting the IPv4.\n")

        elif return_str_error and ip.returncode != 0:
            return "Error collecting the IPv4"

        elif ip.returncode != 0:
            return 1

        else:
            return ip.stdout

    elif ipv6:
        try:
            ip = subprocess.run("curl -6 ifconfig.me", shell=True, capture_output=True, text=True, timeout=5)
        except subprocess.TimeoutExpired:
            ip.returncode = 0

        if return_zhusk_error and ip.returncode != 0:
            raise ZhuskError("\nError collecting the IPv6.\n")

        elif return_str_error and ip.returncode != 0:
            return "Error collecting the IPv6"

        elif ip.returncode != 0:
            return 1

        else:
            return ip.stdout



# Customizations:



def print_slow(text: str, temp: float = 0.02, jump: bool = True) -> None:
    r"""Prints text to the screen, letter by letter, with a typing effect.

    Args:
        text (str): The text that will be displayed.
        temp (float, optional): Wait time between each character, in seconds. Default is 0.02.
        jump (bool, optional): Skips a line at the end of the message (\n). 'True' by default.

    Returns:
        None: This function does not return anything.

    Example:
        >>> zhusk.print_slow("Hello world")
        Hello world
    """

    for letter in text:
        print(letter, end="", flush=True)
        time.sleep(temp)

    if jump:
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
        >>> zhusk.input_slow("Your name: ")
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
