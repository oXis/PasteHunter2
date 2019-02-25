import sys
import re
import argparse
from config import config


def EmailAddress(v):
    # Raise a value error for any part of the string
    # that doesn't match your specification. Make as many
    # checks as you need. I've only included a couple here
    # as examples.
    if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", v):
        # If all the checks pass, just return the string as is
        return v
    else:
        raise argparse.ArgumentTypeError("Must be a valid email address.")


def getParser():
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--phone",
                        help="Phone number to report urgent paste.",
                        action="store",
                        dest="phone",
                        type=str,
                        default=config['report']['number'])

    parser.add_argument("-e", "--email",
                        help="Email address to report to.",
                        action="store",
                        dest="email",
                        type=EmailAddress,
                        default=config['report']['email'])

    parser.add_argument("-r", "--report",
                        help="Delay between reports (in seconds)",
                        action="store",
                        dest="delayReport",
                        type=int,
                        default=config['report']['delay'])

    parser.add_argument("-v", "--verbose",
                        help="Print logs in the terminal",
                        action="store_true",
                        dest="verbose",
                        default=False)

    parser.add_argument("--loadcsv",
                        help="Update filter from CSV file. Exit when done.",
                        action="store",
                        dest="csv",
                        type=str,
                        default=None)

    parser.add_argument("--add",
                        help="Add a filter to the list of filters. Exit when done.",
                        action="store_true",
                        dest="add",
                        default=False)

    # required only if --add is provided
    parser.add_argument("--type",
                        required="--add" in sys.argv,
                        help="Type of filter (card, keyword, email, ...).\
                            Required if --add is provided.",
                        action="store",
                        dest="ftype",
                        type=str)

    parser.add_argument("--regex",
                        required="--add" in sys.argv,
                        help="Regex of filter.\
                            Required if --add is provided.",
                        action="store",
                        dest="regex",
                        type=str)

    parser.add_argument("--urgent",
                        required="--add" in sys.argv,
                        help="1 or 0.\
                            Required if --add is provided.",
                        action="store",
                        dest="urgent",
                        type=int)

    parser.add_argument("--desc",
                        required="--add" in sys.argv,
                        help="Very small description.\
                            Required if --add is provided.",
                        action="store",
                        dest="desc",
                        type=str)

    parser.add_argument('filters',
                        help='json file with filters',
                        action="store",
                        type=str,
                        default="./filters.json")

    return parser
