from datetime import datetime
import json
import os
import typing

import click
from dateutil import parser as dateparse
import tweepy


@click.group
def cli():
    """Tweet the latest data."""
    pass


@cli.command()
def cardinals():
    """Post the latest data."""
    # Open the data
    standings = json.load(open("./data/standings.json", "r"))
    team_standings = next(t for t in standings['205']['teams'] if t['name'] == 'St. Louis Cardinals')

    schedule = json.load(open("./data/schedule.json", "r"))
    games_left = [g for g in schedule if "win_loss_result" not in g]
    until_deadline = [g for g in games_left if dateparse.parse(g['date']) < datetime(2022, 8, 4)]

    projections = json.load(open("./data/fangraphs.json", "r"))

    # Format the message
    message = f"""⚾🧮 @Cardinals Postseason Update 🧮⚾

{team_standings['w']} win{pluralize(team_standings['w'])}
{team_standings['l']} loss{pluralize(team_standings['l'], 'es')}

{len(games_left)} games left
{len(until_deadline)} games until the Aug. 3 trade deadline

{projections['Cardinals']}% chance of making the playoffs, according to @fangraphs
"""

    client = tweepy.Client(consumer_key=os.getenv("TWITTER_CONSUMER_KEY"),
                       consumer_secret=os.getenv("TWITTER_CONSUMER_SECRET"),
                       access_token=os.getenv("TWITTER_ACCESS_TOKEN_KEY"),
                       access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"))

    # Replace the text with whatever you want to Tweet about
    response = client.create_tweet(text=message)

def pluralize(value: typing.Any, arg: str = "s") -> str:
    """Return a plural suffix if the value is not 1, '1', or an object of length 1.
    By default, use 's' as the suffix.
    """
    if "," not in arg:
        arg = "," + arg
    bits = arg.split(",")
    if len(bits) > 2:
        return ""
    singular_suffix, plural_suffix = bits[:2]

    try:
        return singular_suffix if float(value) == 1 else plural_suffix
    except ValueError:  # Invalid string that's not a number.
        pass
    except TypeError:  # Value isn't a string or a number; maybe it's a list?
        try:
            return singular_suffix if len(value) == 1 else plural_suffix
        except TypeError:  # len() of unsized object.
            pass
    return ""
    
if __name__ == "__main__":
    cli()
