import argparse

def print_l(message):
    print(message)

# create the parser
parser = argparse.ArgumentParser(description='Process some integers.')

# add arguments
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer to be processed')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')
parser.add_argument('-say', metavar="MESSAGE", type=str, nargs='+',
                    action=print_l, help="prints the given message")

# parse the arguments
args = parser.parse_args()

# do something with the arguments
result = args.accumulate(args.integers)
print(result)