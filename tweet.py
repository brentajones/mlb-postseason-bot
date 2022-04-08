from datetime import datetime
import json
import os

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
    games_left = [g for g in schedule if not hasattr(g, "win_loss_result")]
    until_deadline = [g for g in games_left if dateparse.parse(g['date']) < datetime(2022, 8, 4)]

    projections = json.load(open("./data/fangraphs.json", "r"))

    # Format the message
    message = f"""⚾🧮 @Cardinals Postseason Update 🧮⚾

{team_standings['w']} wins
{team_standings['l']} losses

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


if __name__ == "__main__":
    cli()
