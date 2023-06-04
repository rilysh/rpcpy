from rpcpy import RPCPy
from time import sleep

# Call a new RPCPy class and pass bot ID
rpc = RPCPy("1114590559970021497")

rpc.rpc_login(True)
rpc.set_activity_details(
    "This is details section"
) 
rpc.set_activity_state(
    "This is state section"
)
rpc.set_activity_timestamp(1807665890, 1807665896)
rpc.set_activity_assets("mm", "large text", "mm", "small text")
rpc.set_is_instance(True)
rpc.set_nonce()
rpc.set_buttons(
    [
        {"label": "Button 1", "url": "https://tinyurl.com/389m7y4k"},
        {"label": "Button 2", "url": "https://tinyurl.com/389m7y4k"}
    ]
)
rpc.rpc_update(True)
sleep(60)
