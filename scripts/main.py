from scripts.top_scraper import Scraper, Channel
from scripts.yt_api import YoutubeAPI
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    filename="logs.log",
    encoding="utf-8",
)


TOP_1000_COUNTRY = (
    "https://us.youtubers.me/{country}/all/top-1000-most-subscribed-youtube-channels-in-{country}"
)


def update_channels_info(channels):
    for idx in range(len(channels)):
        while True:
            try:
                channel: Channel = channels[idx]
                channel_data = yt_api.get_channel_by_name(channel.name)
                channel_id = channel_data["items"][0]["id"]["channelId"]
                channel_region_code = channel_data["regionCode"]
                channel_name = channel_data["items"][0]["snippet"]["title"]
                channel_description = channel_data["items"][0]["snippet"]["description"]
                channel_thumbnail = yt_api.get_thumbnail(channel_data, getsize=False)
                channel.name = channel_name
                channel.url = channel_id
                channel.thumbnail = channel_thumbnail
                channel.description = channel_description
                channel.region_code = channel_region_code
            except Exception:
                logging.info(f"Error retrieving data for channel {channel.name}")
                time.sleep(3)
                continue


if __name__ == "__main__":
    yt_api = YoutubeAPI()
    top_channels = {}
    country = "poland"
    scraper = Scraper(TOP_1000_COUNTRY.format(country=country), country)
    top_channels[country] = scraper.get_top_channels(scraper.url)
    scraper.save_channels()
    country = "united-states"
    scraper = Scraper(TOP_1000_COUNTRY.format(country=country), country)
    top_channels[country] = scraper.get_top_channels(scraper.url)
    scraper.save_channels()
