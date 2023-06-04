### RPCPy
A Python script that uses Discord's UNIX socket to show RPC on profile

### Usage
`set_activity_state(state: str)` - Set activity state string\
`set_activity_details(details: str)` - Set activity details string\
`set_activity_timestamp(start_time: int, end_time: int)` - Set start time and end time in UNIX epoch time format\
`set_activity_assets(large_image: str, large_text: str, small_image: str, small_text: str)` - Set activity RPC image, including hover text\
`set_activity_party(party_id: int, nums: list[int])` - Set activity party information
`set_activity_secrets(join: str, spectate: str, match: str)` - Set activity secrets for others to join the activity\
`set_buttons(obj: object)` - Set buttons on your RPC status\
`set_is_instance(state: bool = True)` - Set the state of the current instance whether is true or false\
`set_nonce()` - Generate nonce key which is also known as UUIDv4 key\
`rpc_login(debug: bool = False)` - Handshake between Discord (client) UNIX socket and RPCPy\
`rpc_logout(debug: bool = False)` - Forcefully disconnect from Discord RPC\
`rpc_update(debug: bool = False)` - Update Discord RPC status

### Example
```py
from rpcpy import RPCPy
from time import sleep


rpc = RPCPy()

rpc.rpc_login(True)
rpc.set_activity_details(
    "This is details and living in quantum space"
)
rpc.set_activity_state(
    "quantum gravitation force where I'm volatile"
)
rpc.set_activity_timestamp(1807665890, 1807665896)
rpc.set_activity_assets("mm", "large text", "mm", "small text")
rpc.set_is_instance(True)
rpc.set_nonce()
rpc.set_buttons(
    [
        {"label": "Button 1", "url": "https://url.org"},
        {"label": "Say Goodbye kid", "url": "https://url.org"}
    ]
)
rpc.rpc_update(True)
sleep(50)
```
This example is also present in `example.py`
