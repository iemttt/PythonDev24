from cowsay import cowsay, Option

import argparse

PRESET_OPTIONS = {
    "b", "d", "g", "p", "s", "t", "w", "y"
}

def get_preset(args):
    return "".join(opt for opt in PRESET_OPTIONS if getattr(args, opt, False))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", help="Select the appearance of the cow's eyes, in which case the first two characters of the argument string eye_string will be used", type=str)
    parser.add_argument("-b", help="Borg mode", action="store_true")
    parser.add_argument("-d", help="Dead mode", action="store_true")
    parser.add_argument("-g", help="Greedy mode", action="store_true")
    parser.add_argument("-p", help="Paranoia mode", action="store_true")
    parser.add_argument("-s", help="Stoned mode", action="store_true")
    parser.add_argument("-t", help="Tired mode", action="store_true")
    parser.add_argument("-w", help="Somewhat the opposite of -t", action="store_true")
    parser.add_argument("-y", help="Brings on the cow's youthful appearance", action="store_true")
    parser.add_argument("message", type=str)

    args = parser.parse_args()
    preset = get_preset(args)
    eyes = args.e[:2] if args.e else Option.eyes
    message = args.message
    print(cowsay(message, preset=preset, eyes=eyes))
