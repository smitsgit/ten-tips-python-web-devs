import asyncio
import datetime

import bs4
import httpx
from colorama import Fore

# Older versions of python require calling loop.create_task() rather than on asyncio.
# Make this available more easily.
loop = None


def main():
    global loop
    loop = asyncio.get_event_loop()

    t0 = datetime.datetime.now()

    loop.run_until_complete(get_title_range_old_version())

    dt = datetime.datetime.now() - t0
    print(f"Done in {dt.total_seconds():.2} sec")


async def get_html(episode_number: int) -> str:
    print(Fore.YELLOW + f"Getting HTML for episode {episode_number}", flush=True)

    url = f'https://talkpython.fm/{episode_number}'

    # The async with syntax ensures that all active connections are closed on exit.
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()

        return resp.text


def get_title(html: str, episode_number: int) -> str:
    print(Fore.CYAN + f"Getting TITLE for episode {episode_number}", flush=True)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    header = soup.select_one('h1')
    if not header:
        return "MISSING"

    return header.text.strip()


async def get_title_range_old_version():
    # Please keep this range pretty small to not DDoS my site. ;)
    for n in range(220, 231):
        html = await get_html(n)
        title = get_title(html, n)
        print(Fore.WHITE + f"Title found: {title}", flush=True)


async def get_title_range():
    # Please keep this range pretty small to not DDoS my site. ;)

    tasks = []
    for n in range(220, 231):
        tasks.append((n, loop.create_task(get_html(n))))

    for n, t in tasks:
        html = await t
        title = get_title(html, n)
        print(Fore.WHITE + f"Title found: {title}", flush=True)


if __name__ == '__main__':
    main()
