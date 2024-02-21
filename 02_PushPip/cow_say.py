from cowsay import cowsay

import argparse

PRESET_OPTIONS = {
    "b", "d", "g", "p", "s", "t", "w", "y"
}

def get_preset(args):
    return "".join(opt for opt in PRESET_OPTIONS if getattr(args, opt, False))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("message", type=str)
    parser.add_argument("-b", help="Borg mode", action="store_true")
    parser.add_argument("-d", help="Dead mode", action="store_true")
    parser.add_argument("-g", help="Greedy mode", action="store_true")
    parser.add_argument("-p", help="Paranoia mode", action="store_true")
    parser.add_argument("-s", help="Stoned mode", action="store_true")
    parser.add_argument("-t", help="Tired mode", action="store_true")
    parser.add_argument("-w", help="Somewhat the opposite of -t", action="store_true")
    parser.add_argument("-y", help="Brings on the cow's youthful appearance", action="store_true")

    args = parser.parse_args()
    preset = get_preset(args)
    message = args.message

    print(cowsay(message, preset=preset))
