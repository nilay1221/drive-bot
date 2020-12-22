from telethon import TelegramClient,events,types,functions,Button
import sys
from drive_upload import uploadFile
import os
import asyncio
import concurrent.futures
from downloader import Downloader
from enum import Enum,auto
import logging


api_id = '' #ADD API ID
api_hash = '' #ADD API HASH
bot_token = '' #ADD BOT TOKEN if using bot
client = TelegramClient('bot',api_id,api_hash).start(bot_token=bot_token)

root = logging.getLogger(__name__)
root.setLevel(logging.DEBUG)

logger = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.DEBUG)
root.addHandler(logger)



class ProgressPercentage:

    def __init__(self,msg,total:int):
        self.filed_len = 0
        self.percents = 0
        self.msg = msg
        self.bar_len = 25
        self.base = 20
        self.total = total


    
    def progress(self,count, total, suffix=''):
        percents = round(100.0 * count / float(total))
        percents = self.base * round(percents/self.base)
        filled_len = int(round((percents*self.bar_len)/100))
        return (filled_len,percents)

    
    async def __call__(self,recvd_bytes):
        # root.debug("Downloaded %d bytes",recvd_bytes)
        filled_len,percents = self.progress(recvd_bytes,self.total)
        if self.filed_len != filled_len or self.percents != percents:
            self.filed_len = filled_len
            self.percents = percents
            bar = '=' * filled_len + '-' * (self.bar_len - filled_len)
            await client.edit_message(self.msg,f"Downloading " + f"[{bar}] {percents}%")


    
    
sem = asyncio.Semaphore(value=1)
    

async def _downloadFile(client:TelegramClient,file:types.InputDocumentFileLocation,offset:int,limit:int):
        print('Downloading')
        down = await client(functions.upload.GetFileRequest(location=file,offset=offset,limit=limit))
        print('Downloading completed')
        return down.bytes


@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.message.media:
        res = event.message
        msg = await event.message.reply('Downloading Starting')
        file_name = event.message.file.name
        mime_type = event.message.media.document.mime_type
        path = os.getcwd() + '/uploads/' + file_name 
        media = res.media.document
        file = types.InputDocumentFileLocation(
            id=media.id,
            access_hash=media.access_hash,
            file_reference = media.file_reference,
            thumb_size=''
        );
        file_size = media.size
        progress = ProgressPercentage(msg,file_size)
        d = Downloader(client,file,file_size,media.dc_id)
        await d.download(path,progress)
        print('\n' +path)
        print('now uploading')
        await client.edit_message(msg,'File downloaded')
        await client.edit_message(msg,'Uploading Starting')
        loop = asyncio.get_running_loop()
        size = float(os.path.getsize(path))
        async with sem:
            print('Uploading')
            url = await loop.run_in_executor(None,uploadFile,path,file_name,mime_type)
            print('Upload Complete')
        await client.edit_message(msg,'Upload Complete');
        os.remove(path)


client.run_until_disconnected()