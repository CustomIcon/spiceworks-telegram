from configparser import ConfigParser
from io import BytesIO
from os import path

from aiohttp import ClientSession
from pyrogram import Client

config = ConfigParser()
with open('config.ini') as configFile:
    config.read_file(configFile)


class bot(Client):
    def __init__(
        self,
        name: str,
        api_id: int = config.getint('spiceworks-bot', 'id'),
        api_hash: str = config.get('spiceworks-bot', 'hash'),
        auth: str = config.get('spiceworks-help-desk', 'auth'),
        cookies: str = config.get('spiceworks-help-desk', 'set_cookies'),
        host: str = config.get('spiceworks-help-desk', 'host'),
        aioclient = ClientSession,
    ):
        self.plugins = {'root': path.join(__package__, 'plugins')}
        self.host = host
        self.url = f"http://{self.host}"
        self.auth = auth
        self.cookie = cookies
        self.aioclient = aioclient(
            headers={
                'User-Agent': 'Spiceworks Android mobile - phone',
                'Authorization': f'Basic {self.auth}',
                'Cookie': self.cookie,
                'Host': self.host,
                'Connection': 'Keep-Alive'
            }
        )

        super().__init__(
            name,
            api_id=api_id,
            api_hash=api_hash,
            workers=16,
            plugins=self.plugins,
            workdir="./",
        )
    
    async def get_tickets(self, ticket_id: int = None):
        req = await self.aioclient.get(
            f'{self.url}/api/tickets/{ticket_id}.json'
        ) if ticket_id else await self.aioclient.get(
            f'{self.url}/api/tickets.json'
        )
        return await req.json()

    async def close_ticket(self, ticket_id: int):
        ...
    
    async def reopen_ticket(self, ticket_id: int):
        ...
    
    async def comment(self, ticket_id, text: str = None, media: bool = False):
        ...
    
    
    