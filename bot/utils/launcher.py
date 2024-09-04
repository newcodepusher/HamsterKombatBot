import os
import glob
import asyncio
import argparse

from bot.config import settings
from bot.utils import logger
from bot.core.tapper import run_tapper


start_text = """

▒█ ▒█ █▀▀█ █▀▄▀█ █▀▀ ▀▀█▀▀ █▀▀ █▀▀█ ▒█ ▄▀ █▀▀█ █▀▄▀█ █▀▀▄ █▀▀█ ▀▀█▀▀ ▒█▀▀█ █▀▀█ ▀▀█▀▀ 
▒█▀▀█ █▄▄█ █ ▀ █ ▀▀█   █   █▀▀ █▄▄▀ ▒█▀▄  █  █ █ ▀ █ █▀▀▄ █▄▄█   █   ▒█▀▀▄ █  █   █   
▒█ ▒█ ▀  ▀ ▀   ▀ ▀▀▀   ▀   ▀▀▀ ▀ ▀▀ ▒█ ▒█ ▀▀▀▀ ▀   ▀ ▀▀▀  ▀  ▀   ▀   ▒█▄▄█ ▀▀▀▀   ▀  

Select an action:

    1. Create session
    2. Run bot
"""


def get_url_names() -> list[str]:
    url_names = glob.glob('sessions/*.txt')
    url_names = [file for file in url_names]

    return url_names


async def get_sessions() -> list[dict]:
    url_names = get_url_names()

    result = []

    for url_name in url_names:
        print("url_name", url_name)
        f = open(url_name, "r")
        session = {"name": os.path.splitext(os.path.basename(url_name)), "url": f.read()}
        result.append(session)
        f.close()

    return result


async def process() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--action', type=int, help='Action to perform')

    logger.info(f"Detected {len(get_url_names())} urls")

    sessions = await get_sessions()
    await run_tasks(sessions=sessions)


async def run_tasks(sessions: list[dict]):
    tasks = [asyncio.create_task(run_tapper(session=session))
             for session in sessions]

    await asyncio.gather(*tasks)
