from telethon import TelegramClient,functions,types
from telethon.tl.types import InputDocumentFileLocation
from telethon.network import MTProtoSender
import asyncio
import time
import logging
from typing import BinaryIO,Callable


class Downloader:

    def __init__(self,client:TelegramClient,file:InputDocumentFileLocation,file_size:int,dc_id:int):
        self.client = client
        self.sender = self.client._sender
        self.file = file
        self.dc_id = dc_id
        self.file_size = file_size
        self.exported = dc_id and self.client.session.dc_id != dc_id
        self.sem = asyncio.Semaphore(value=5)
        self.totalDownload = 0

    async def _download(self,request:functions.upload.GetFileRequest,offset:int,f:BinaryIO,callback:Callable):
        async with self.sem:
            results = await self.client._call(self.sender,request)
            f.seek(offset)
            f.write(results.bytes)
            self.totalDownload += len(results.bytes)
            if callback is not None:
                await callback(self.totalDownload)



    async def download(self,path:str,callback:Callable=None):
        if self.exported:
            self.sender = await self.client._borrow_exported_sender(self.dc_id)

        downloads = []
        offset = 0
        limit = 512*1024
        with open(path,'wb') as f:
            while offset < self.file_size:
                downloads.append(self._download(functions.upload.GetFileRequest(
                    location=self.file,
                    offset=offset,
                    limit=limit
                ),offset,f,callback))
                offset += limit
            results = await asyncio.gather(*downloads)
            print(results)