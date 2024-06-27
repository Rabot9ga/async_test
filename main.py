import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
import time

lst_of_games = []
async def get_url(i):
    global lst_of_games
    async with aiohttp.ClientSession() as session:
        async with session.get('https://psprices.com/region-tr/collection/all-discounts?page=' + str(i)) as resp:
            print(i)
            soup = BeautifulSoup(await resp.text(), 'html.parser')
            lst_of_games.extend([i['href'] for i in soup.find_all('a',
                    'flex flex-col gap-1 relative mt-1 z-10 focus:ring rounded text-text group')])


async def http_test(url):
    async with aiohttp.ClientSession() as session:
        async  with session.get('https://psprices.com'+url) as resp:
            print(resp.status)


async def async_main():
    global lst_of_games
    await asyncio.gather(*(get_url(i) for i in range(1, 4)))
    await asyncio.gather(*(http_test(i) for i in lst_of_games))



def get_urls_games():
    global lst_of_games
    for i in range(1, 4):
        response = requests.get('https://psprices.com/region-tr/collection/all-discounts?page=' + str(i))
        soup = BeautifulSoup(response.text, 'html.parser')
        lst_of_games.extend([i['href'] for i in soup.find_all('a',
                                                              'flex flex-col gap-1 relative mt-1 z-10 focus:ring rounded text-text group')])
        print(i)
def get_respons_stat():
    global lst_of_games
    for i in lst_of_games:
        print(requests.get('https://psprices.com'+i).status_code)


def main():
    get_urls_games()
    get_respons_stat()

if __name__ == "__main__":
    start = time.time()
    asyncio.run(async_main())
    # main()
    print(time.time()-start)