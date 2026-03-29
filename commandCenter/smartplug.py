import asyncio
import threading
from aioesphomeapi import APIClient


class SmartPlug:
    def __init__(self, ip):
        self.ip = ip
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._start_loop, daemon=True)
        self._thread.start()

        self._state = None
        self._switch_key = None

        self._loop.call_soon_threadsafe(asyncio.create_task, self._connect())

    def _start_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    async def _connect(self):
        self.client = APIClient(self.ip, 6053, None)
        await self.client.connect(login=True)

        entities, _ = await self.client.list_entities_services()

        for e in entities:
            if e.object_id == "kauf_plug":
                self._switch_key = e.key

        def on_state(state):
            if state.key == self._switch_key:
                self._state = state.state

        self.client.subscribe_states(on_state)

    def _run(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self._loop)

    def get_state(self):
        return self._state

    def turn_on(self):
        self.client.switch_command(self._switch_key, True)

    def turn_off(self):
        self.client.switch_command(self._switch_key, False)

    def toggle(self):
        current = self._state if self._state is not None else False
        self.client.switch_command(self._switch_key, not current)