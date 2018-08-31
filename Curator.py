"""
Commandline version of CommentGatherer module.

_Usage_

## Gathering newer comments to put into database

$python Curator.py 'database name' 'client id' 'client secret' 'gather'
    -l 100

This gathers the latest 100 comments from ask historians.

## Checking if comments in database have since been removed

$python Curator.py 'database name' 'client id' 'client secret' 'check'
    -s 7
Checks all comments younger than seven days, to see if they have been removed
"""
import CommentGatherer as cg
import sys
import argparse


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('db_name', help='Database Name')
    parser.add_argument('client_id', help='Reddit Client ID')
    parser.add_argument('client_secret', help='Reddit Client Secret')
    parser.add_argument('action', help='Flag for which action to perform')

    limit_str = 'Number of Reddit comments to download'
    parser.add_argument('-l', '--limit', type=int, help=limit_str)
    stale_str = 'Number of days after which comment will not be removed'
    parser.add_argument('-s', '--stale', type=int, help=stale_str)

    args = parser.parse_args(argv)
    gatherer, reddit_instance = start_up(args.db_name, args.client_id,
                                         args.client_secret)
    if args.action == 'gather':
        Gather(gatherer, reddit_instance, args.limit)
    elif args.action == 'check':
        Checker(gatherer, reddit_instance, args.stale)
    else:
        raise ValueError('Unrecognised action')


def start_up(db_name, client_id_val, client_secret_val):
    gatherer = cg.Gatherer(db_name)
    reddit_instance = gatherer.connect(client_id_val, client_secret_val)
    return gatherer, reddit_instance


def Gather(gatherer, reddit_instance, limit):
    print('Gathering comments...')
    gatherer.gather_comments(reddit_instance, limit)
    print('Gathering Complete')


def Checker(gatherer, reddit_instance, stale_days):
    print('Checking comments...')
    gatherer.check_stale_comments(reddit_instance, stale_days)
    print('Checking Complete')


if __name__ == '__main__':
    main()
