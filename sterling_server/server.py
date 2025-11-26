import asyncio
import logging
import os
from .cache import SterlingCache

class SterlingServer:
    def __init__(
        self,
        host='localhost',
        port=9162,
        persistence_mode='RDB',
        maxmemory=None,
        eviction_policy='noeviction',
        log_to_file=False,
        log_file_path=None,
        fresh_logs=False
    ):
        self.host = host
        self.port = port
        self.cache = SterlingCache(
            persistence_mode=persistence_mode,
            maxmemory=maxmemory,
            eviction_policy=eviction_policy
        )
        self._setup_logging(log_to_file, log_file_path, fresh_logs)
        self.logger = logging.getLogger('sterling_server')

    def _setup_logging(self, log_to_file, log_file_path, fresh_logs):
        logger = logging.getLogger('sterling_server')
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if log_to_file:
            if not log_file_path:
                os.makedirs('log', exist_ok=True)
                log_file_path = 'log/server_logs.log'
            mode = 'w' if fresh_logs else 'a'
            file_handler = logging.FileHandler(log_file_path, mode=mode)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        else:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        self.logger.info(f"Client connected: {addr}")
        
        try:
            while True:
                data = await reader.readline()
                if not data:
                    break
                
                command = data.decode().strip()
                if not command:
                    continue
                
                self.logger.debug(f"Command from {addr}: {command}")
                response = await self.cache.execute_command(command)
                writer.write((response + '\n').encode())
                await writer.drain()
                
        except Exception as e:
            self.logger.error(f"Error handling client {addr}: {e}")
        finally:
            self.logger.info(f"Client disconnected: {addr}")
            writer.close()
            await writer.wait_closed()

    async def start(self):
        await self.cache.load()
        server = await asyncio.start_server(
            self.handle_client, self.host, self.port
        )
        self.logger.info(f"Sterling Cache Server running on {self.host}:{self.port}")
        async with server:
            await server.serve_forever()

    def run(self):
        try:
            asyncio.run(self.start())
        except KeyboardInterrupt:
            self.logger.info("Server shutting down...")
