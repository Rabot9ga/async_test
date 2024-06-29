import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
import time
import logging
class ColoredFormatter(logging.Formatter):
    COLORS = {'DEBUG': '\033[94m', 'INFO': '\033[92m', 'WARNING': '\033[93m',
              'ERROR': '\033[91m', 'CRITICAL': '\033[95m'}

    def format(self, record):
        log_fmt = f"{self.COLORS.get(record.levelname, '')} 📊 %(levelname)s - ⏳ %(asctime)s - ⚠️ %(funcName)s - 📝 line: %(lineno)d - 💬 %(message)s\033[0m"
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

logging.basicConfig(level=logging.NOTSET, handlers=[logging.StreamHandler()])
logging.getLogger().handlers[0].setFormatter(ColoredFormatter())

lst_of_games = []
async def get_url(i):
    global lst_of_games
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('https://psprices.com/region-tr/collection/all-discounts?page=' + str(i)) as resp:
                soup = BeautifulSoup(await resp.text(), 'html.parser')
                lst_of_games.extend([i['href'] for i in soup.find_all('a',
                        'flex flex-col gap-1 relative mt-1 z-10 focus:ring rounded text-text group')])
                logging.critical(f"Страница {i}: status code {resp.status}")
        except Exception as e:
            logging.error(str(e))
        else:
            pass


async def http_test(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('https://psprices.com'+url) as resp:
                soup = BeautifulSoup(await resp.text(), 'html.parser')
                logging.info(f"Игра - {url.split('/')[-1]}: status code {resp.status}")
        except Exception as e:
            logging.error(str(e))
        else:
            pass

async def async_main():
    global lst_of_games
    await asyncio.gather(*(get_url(i) for i in range(1, 3)))
    await asyncio.gather(*(http_test(i) for i in lst_of_games))


def get_urls_games():
    global lst_of_games
    for i in range(1, 3):
        try:
            response = requests.get('https://psprices.com/region-tr/collection/all-discounts?page=' + str(i))
            soup = BeautifulSoup(response.text, 'html.parser')
            lst_of_games.extend([i['href'] for i in soup.find_all('a',
                        'flex flex-col gap-1 relative mt-1 z-10 focus:ring rounded text-text group')])
            logging.critical(f"Страница {i}: status code {response.status_code}")
        except Exception as e:
            logging.error(str(e))
        else:
            pass

def get_respons_stat():
    global lst_of_games
    for i in lst_of_games:
        try:
            resp = requests.get('https://psprices.com'+i)
            soup = BeautifulSoup(resp.text, 'html.parser')
            logging.info(f"Игра - {i.split('/')[-1]}: status code {resp.status_code}")
        except Exception as e:
            logging.error(str(e))
        else:
            pass

def main():
    get_urls_games()
    get_respons_stat()

if __name__ == "__main__":
    logging.debug("‼️Started‼️")
    start = time.time()
    asyncio.run(async_main())
    # main()
    logging.debug("‼️Ended‼️")
    logging.critical(f'Время выполнения кода: {time.time()-start:.2f} секунд')