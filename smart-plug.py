import asyncio
from aioesphomeapi import APIClient

async def main():
    client = APIClient("192.168.137.92", 6053, None)
    await client.connect(login=True)

    entities, services = await client.list_entities_services()

    # Find switch key
    switch_key = None
    for e in entities:
        if e.object_id == "kauf_plug":
            switch_key = e.key

    # Store latest states
    states = {}

    def on_state(state):
        states[state.key] = state.state

    # Subscribe to state updates
    client.subscribe_states(on_state)
    # Give it a moment to receive current state
    await asyncio.sleep(1)

    current = states.get(switch_key)
    print("Current state:", current)

    # Toggle
    new_state = not current
    print("Toggling to:", new_state)
    client.switch_command(switch_key, new_state)

asyncio.run(main())