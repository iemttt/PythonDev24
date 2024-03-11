from cowsay import cowsay, Option, list_cows, read_dot_cow, make_bubble, THOUGHT_OPTIONS

import argparse
from sys import stdin
import os
import os.path
from typing import Optional, Set, Tuple

import cmd
import shlex

PRESET_OPTIONS: Set[str] = {
    "b", "d", "g", "p", "s", "t", "w", "y"
}


def get_preset(args: argparse.Namespace):
    return "".join(opt for opt in PRESET_OPTIONS if getattr(args, opt, False))


def get_cow(arg: str) -> Tuple[Optional[str], Optional[str]]:
    cow: str = "default"
    cowfile: str = None
    
    if arg is None:
        return cow, cowfile

    if os.sep in arg:
        cow = None
        # arg is a path to cowfile
        if os.path.exists(arg):
            with open(arg) as f:
                cowfile = read_dot_cow(f)
            return cow, cowfile
    else:
        # arg is a cowfile name
        cow = arg
        if cow in list_cows():
            return cow, cowfile

    raise FileNotFoundError(f"Could not find {arg} cowfile!")


class CowSay(cmd.Cmd):
    prompt = "CowSay>"

    def do_cowsay(self, arg):
        print(cowsay(arg))

    def do_list_cows(self, _):
        print(*list_cows())
    
    def do_make_bubble(self, arg):
        args = shlex.split(arg)
        brackets_options = ["cowsay", "cowthink"]
        brackets = "cowsay"
        width = 40
        wrap_text = True
        message = arg[0]
        next_is_arg = False
        for i, a in enumerate(args):
            if a == "-b":
                if args[i+1] in brackets_options:
                    brackets = args[i+1]
                else:
                    print(f"-b options: {shlex.quote(shlex.join(brackets_options))}")
                    return
                next_is_arg = True
            elif a == "-w":
                try:
                    width = int(args[i+1])
                except ValueError:
                    print("-w needs integer value")
                    return
                next_is_arg = True
            elif a == "-n":
                wrap_text == False
            else:
                message = a
                next_is_arg = False
        print(
            make_bubble(
                message,
                brackets=THOUGHT_OPTIONS[brackets],
                width=width,
                wrap_text=wrap_text
            )
        )


if __name__ == '__main__':
    CowSay().cmdloop()

    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("-e", dest="eyes", help="Select the appearance of the cow's eyes, in which case the first two characters of the argument string will be used", type=str)
    parser.add_argument("-T", dest="tongue", help="Select the appearance of the cow's tongue, in which case the first two characters of the argument string will be used", type=str)
    parser.add_argument("-b", help="Borg mode", action="store_true")
    parser.add_argument("-d", help="Dead mode", action="store_true")
    parser.add_argument("-g", help="Greedy mode", action="store_true")
    parser.add_argument("-p", help="Paranoia mode", action="store_true")
    parser.add_argument("-s", help="Stoned mode", action="store_true")
    parser.add_argument("-t", help="Tired mode", action="store_true")
    parser.add_argument("-w", help="Somewhat the opposite of -t", action="store_true")
    parser.add_argument("-y", help="Brings on the cow's youthful appearance", action="store_true")
    parser.add_argument("-W", dest="width", help="specifies roughly where the message should be wrapped. The default is equivalent to -W 40 i.e. wrap words at or before the 40th column.", type=int, default=40)
    parser.add_argument("-n", dest="no_wrap_text", help="If it is specified, the given message will not be word-wrapped", action="store_true")
    parser.add_argument("-l", dest="list_all_cows", help="Lists all cows", action="store_true")
    parser.add_argument("-f", dest="cowfile", help="Option specifies a particular cow picture file (\"cowfile\") to use. If the cowfile spec contains '/' then it will be interpreted as a path relative to the current directory. Otherwise, cowsay will search cowfile among available options that can be see with -l option", type=str)
    parser.add_argument("message", type=str, nargs="?")
    args: argparse.Namespace = parser.parse_args()

    if args.list_all_cows:
        print("Cow files in cowsay-python:")
        print(*list_cows())
        exit()
    
    if args.message is None:
        message = stdin.read()
    else:    
        message = args.message

    preset: str = get_preset(args)
    eyes: str = args.eyes[:2] if args.eyes else Option.eyes
    tongue: str = args.tongue[:2] if args.tongue else Option.tongue
    width: int = args.width
    wrap_text: bool = args.no_wrap_text
    cow, cowfile = get_cow(args.cowfile)

    print(cowsay(
        message=message,
        preset=preset,
        eyes=eyes,
        tongue=tongue,
        width=width,
        wrap_text=wrap_text,
        cow=cow,
        cowfile=cowfile
        )
    )
