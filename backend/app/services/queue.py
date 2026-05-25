import sqlite3
import json
import time
import os
from abc import ABC, abstractmethod

class TraceQueue(ABC):
    @abstractmethod
    async def push(self, trace_data: dict):
        pass

    @abstractmethod
    async def pop(self) -> dict:
        pass

class SQLiteTraceQueue(TraceQueue):
    def __init__(self, db_path="queue.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS queue (id INTEGER PRIMARY KEY, data TEXT)")

    async def push(self, trace_data: dict):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO queue (data) VALUES (?)", (json.dumps(trace_data),))

    async def pop(self) -> dict:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT id, data FROM queue ORDER BY id LIMIT 1")
            row = cursor.fetchone()
            if row:
                conn.execute("DELETE FROM queue WHERE id = ?", (row[0],))
                return json.loads(row[1])
        return None

import redis

class RedisTraceQueue(TraceQueue):
    def __init__(self):
        self.host = os.getenv("REDIS_HOST", "localhost")
        self.port = int(os.getenv("REDIS_PORT", 6379))
        self.queue_name = "llm_traces"
        self._client = None
        self.is_available = False
        self._check_connection()

    def _check_connection(self):
        try:
            self._client = redis.Redis(host=self.host, port=self.port, socket_connect_timeout=1)
            self._client.ping()
            self.is_available = True
        except Exception:
            self.is_available = False

    async def push(self, trace_data: dict):
        if not self.is_available:
            raise ConnectionError("Redis not available")
        self._client.rpush(self.queue_name, json.dumps(trace_data))

    async def pop(self) -> dict:
        if not self.is_available:
            return None
        data = self._client.blpop(self.queue_name, timeout=1)
        if data:
            return json.loads(data[1])
        return None

def get_trace_queue() -> TraceQueue:
    rq = RedisTraceQueue()
    if rq.is_available:
        return rq
    return SQLiteTraceQueue()
