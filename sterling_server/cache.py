import asyncio
import pickle
import os
import time
from collections import OrderedDict

class SterlingCache:
    def __init__(self, persistence_mode='RDB', maxmemory=None, eviction_policy='noeviction'):
        self.data = OrderedDict()
        self.ttl = {}
        self.lock = asyncio.Lock()
        self.persistence_mode = persistence_mode
        self.maxmemory = maxmemory
        self.eviction_policy = eviction_policy
        self.aof_file = 'sterling.aof'
        self.rdb_file = 'sterling.rdb'

    async def execute_command(self, command):
        parts = command.split(maxsplit=2)
        if not parts:
            return "ERR empty command"
        
        cmd = parts[0].upper()
        
        try:
            if cmd == 'SET' and len(parts) >= 3:
                key, value = parts[1], parts[2]
                await self.set(key, value)
                return "OK"
            elif cmd == 'GET' and len(parts) == 2:
                value = await self.get(parts[1])
                return value if value is not None else "(nil)"
            elif cmd == 'DEL' and len(parts) == 2:
                await self.delete(parts[1])
                return "OK"
            elif cmd == 'EXISTS' and len(parts) == 2:
                exists = await self.exists(parts[1])
                return "1" if exists else "0"
            elif cmd == 'EXPIRE' and len(parts) == 3:
                await self.expire(parts[1], int(parts[2]))
                return "OK"
            elif cmd == 'TTL' and len(parts) == 2:
                ttl_val = await self.get_ttl(parts[1])
                return str(ttl_val)
            elif cmd == 'KEYS':
                keys = await self.keys()
                return ' '.join(keys) if keys else "(empty)"
            else:
                return "ERR unknown command"
        except Exception as e:
            return f"ERR {str(e)}"

    async def set(self, key, value):
        async with self.lock:
            self._check_eviction()
            self.data[key] = value
            if key in self.ttl:
                del self.ttl[key]
        await self._persist_write(f"SET {key} {value}")

    async def get(self, key):
        async with self.lock:
            if key in self.ttl and time.time() > self.ttl[key]:
                del self.data[key]
                del self.ttl[key]
                return None
            return self.data.get(key)

    async def delete(self, key):
        async with self.lock:
            if key in self.data:
                del self.data[key]
            if key in self.ttl:
                del self.ttl[key]
        await self._persist_write(f"DEL {key}")

    async def exists(self, key):
        async with self.lock:
            if key in self.ttl and time.time() > self.ttl[key]:
                del self.data[key]
                del self.ttl[key]
                return False
            return key in self.data

    async def expire(self, key, seconds):
        async with self.lock:
            if key in self.data:
                self.ttl[key] = time.time() + seconds
        await self._persist_write(f"EXPIRE {key} {seconds}")

    async def get_ttl(self, key):
        async with self.lock:
            if key not in self.data:
                return -2
            if key not in self.ttl:
                return -1
            remaining = int(self.ttl[key] - time.time())
            return max(remaining, -2)

    async def keys(self):
        async with self.lock:
            return list(self.data.keys())

    def _check_eviction(self):
        if self.maxmemory and len(self.data) >= self.maxmemory:
            if self.eviction_policy == 'lru':
                self.data.popitem(last=False)
            elif self.eviction_policy == 'allkeys-lru':
                self.data.popitem(last=False)

    async def _persist_write(self, command):
        if self.persistence_mode == 'AOF':
            with open(self.aof_file, 'a') as f:
                f.write(command + '\n')
        elif self.persistence_mode == 'RDB':
            await self.save_snapshot()

    async def save_snapshot(self):
        temp_file = self.rdb_file + '.tmp'
        async with self.lock:
            with open(temp_file, 'wb') as f:
                pickle.dump({'data': dict(self.data), 'ttl': self.ttl}, f)
        os.replace(temp_file, self.rdb_file)

    async def load(self):
        if self.persistence_mode == 'RDB' and os.path.exists(self.rdb_file):
            with open(self.rdb_file, 'rb') as f:
                snapshot = pickle.load(f)
                self.data = OrderedDict(snapshot['data'])
                self.ttl = snapshot['ttl']
        elif self.persistence_mode == 'AOF' and os.path.exists(self.aof_file):
            with open(self.aof_file, 'r') as f:
                for line in f:
                    await self.execute_command(line.strip())
