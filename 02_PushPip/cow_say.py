from cowsay import cowsay, Option

import argparse
from sys import stdin


PRESET_OPTIONS = {
    "b", "d", "g", "p", "s", "t", "w", "y"
}

def get_preset(args):
    return "".join(opt for opt in PRESET_OPTIONS if getattr(args, opt, False))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", help="Select the appearance of the cow's eyes, in which case the first two characters of the argument string will be used", type=str)
    parser.add_argument("-T", help="Select the appearance of the cow's tongue, in which case the first two characters of the argument string will be used", type=str)
    parser.add_argument("-b", help="Borg mode", action="store_true")
    parser.add_argument("-d", help="Dead mode", action="store_true")
    parser.add_argument("-g", help="Greedy mode", action="store_true")
    parser.add_argument("-p", help="Paranoia mode", action="store_true")
    parser.add_argument("-s", help="Stoned mode", action="store_true")
    parser.add_argument("-t", help="Tired mode", action="store_true")
    parser.add_argument("-w", help="Somewhat the opposite of -t", action="store_true")
    parser.add_argument("-y", help="Brings on the cow's youthful appearance", action="store_true")
    parser.add_argument("-W", help="specifies roughly where the message should be wrapped. The default is equivalent to -W 40 i.e. wrap words at or before the 40th column.", type=int)
    parser.add_argument("-n", help="If it is specified, the given message will not be word-wrapped", action="store_true")
    parser.add_argument("message", type=str, nargs="?")
    args = parser.parse_args()
    
    if args.message is None:
        message = stdin.read()
    else:    
        message = args.message

    preset = get_preset(args)
    eyes = args.e[:2] if args.e else Option.eyes
    tongue = args.T[:2] if args.T else Option.tongue
    width = args.W if args.W else 40
    wrap_text = args.n
    
    print(cowsay(
        message=message,
        preset=preset,
        eyes=eyes,
        tongue=tongue,
        width=width,
        wrap_text=wrap_text,
        )
    )
