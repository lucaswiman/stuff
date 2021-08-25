import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--some-arg', required=True)
args = parser.parse_args()
do_the_thing(args.some_arg)
