from json import dumps, loads
from struct import pack
from socket import socket, SocketType, AF_UNIX, SOCK_STREAM
from typing_extensions import Any, Self
from os import getpid, access, F_OK
from uuid import uuid4

class RPCPy:
    """
        Initialize all base variables and setup dicts
    """
    def __init__(self: Self, client_id: str) -> None:
        self.EXIT_ERROR = 1
        self.PATH = "/run/user/1000/discord-ipc-0"
        self.RPC_OBJ = {}
        self.LOGOUT_DATA = {"v": 2}
        self.LOGIN_DATA = {"v": 1, "client_id": client_id}

        self.RPC_OBJ["cmd"] = "SET_ACTIVITY"
        self.RPC_OBJ["args"] = {}
        self.RPC_OBJ["args"]["activity"] = {}
        self.RPC_OBJ["args"].update({
            "pid": getpid()
        })

        self.sock = socket(AF_UNIX, SOCK_STREAM)
        if access(self.PATH, F_OK):
            self.sock.connect(self.PATH)
        else:
            print("Error: Discord's IPC socket wasn't found")
            exit(self.EXIT_ERROR)

    """
        Function: __encode__(opcode, payload) (private)
        Used to encode dict payload before sending to Discord client
    """
    def __encode__(self: Self, opcode: int, payload: Any) -> bytes:
        payload = dumps(payload).encode("utf-8")
        return pack("<ii", opcode, len(payload)) + payload
    
    """
        Function: sock_send(sock, opcode, debug, payload) (private)
        Used to send encoded payload to Discord's UNIX socket (which is created by the client)
    """
    def sock_send(
            self: Self, sock: SocketType,
            opcode: int, debug: bool, payload: Any
    ) -> None:
        enc_payload = self.__encode__(opcode, payload)
        try:
            sock.send(enc_payload)
            recv = sock.recv(1024)
            if debug:
                jn = loads(recv[8:])
                if "user" in jn["data"]:
                    user_id = jn["data"]["user"]["id"]
                    user_name = jn["data"]["user"]["username"]
                    is_bot = jn["data"]["user"]["bot"]
                    print(
                        f"ID: {user_id}\n"
                        f"Username: {user_name}\n"
                        f"Bot: {is_bot}"
                    )
        except Exception:
            raise Exception("Error: Failed to send payload to Discord socket")

    """
        Function: set_activity_state(state)
        Used to set activity state for RPC
    """
    def set_activity_state(self: Self, state: str) -> None:
        self.RPC_OBJ["args"]["activity"].update({
            "state": state
        })

    """
        Function: set_activity_details(details)
        Used to set activity details for RPC
    """
    def set_activity_details(self: Self, details: str) -> None:
        self.RPC_OBJ["args"]["activity"].update({
            "details": details
        })

    """
       Function: set_activity_timestamp(start_time, end_time)
       Used to set activity timestamps (starting and ending) and must be in UNIX timestamp format
    """
    def set_activity_timestamp(
            self: Self, start_time: int, end_time: int
    ) -> None:
        self.RPC_OBJ["args"]["activity"]["timestamps"] = {}
        self.RPC_OBJ["args"]["activity"]["timestamps"].update ({
            "start": start_time,
            "end": end_time
        })

    """
        Function: set_activity_assets(large_image, large_text, small_image, small_text)
        Used to set activity assets which includes images and the text which will be shown when a user will hover on them
    """
    def set_activity_assets(
            self: Self, large_image: str,
            large_text: str, small_image: str,
            small_text: str
    ) -> None:
        self.RPC_OBJ["args"]["activity"]["assets"] = {}
        self.RPC_OBJ["args"]["activity"]["assets"].update({
            "large_image": large_image,
            "large_text": large_text,
            "small_image": small_image,
            "small_text": small_text
        })

    """
        Function: set_activity_party(party_id, nums)
        Used to set game party information, e.g. In which level you're in right now
    """
    def set_activity_party(
            self: Self, party_id: str, nums: list[int]
    ) -> None:
        self.RPC_OBJ["args"]["activity"]["party"] = {}
        self.RPC_OBJ["args"]["activity"]["party"].update({
            "id": party_id,
            "size": nums
        })

    """
        Function: set_activity_secrets(join, spectate, match)
        Used to set activity secrets. These are the keys used when a user want to show what activity they're doing
    """
    def set_activity_secrets(
            self: Self, join: str,
            spectate: str, match: str
    ) -> None:
        self.RPC_OBJ["args"]["activity"]["secrets"] = {}
        self.RPC_OBJ["args"]["activity"]["secrets"].update({
            "join": join,
            "spectate": spectate,
            "match": match
        })

    """
        Function: set_buttons(obj)
        Used to add buttons on RPC. Buttons must be passed inside an array
    """
    def set_buttons(self: Self, obj: object) -> None:
        self.RPC_OBJ["args"]["activity"].update({
            "buttons": obj
        })

    """
        Function: set_is_instance(state)
        Used to set if it's an instance or not. Default value is True
    """
    def set_is_instance(self: Self, state: bool = True) -> None:
        self.RPC_OBJ["args"]["activity"].update({
            "instance": state
        })

    """
        Function: set_nonce()
        Used to create nonce key which can be refer as a UUID v4 key.
    """
    def set_nonce(self: Self) -> None:
       self.RPC_OBJ["nonce"] = str(uuid4())

    """
        Function: rpc_login(debug)
        Used to login (handshake) to between RPCPy and Discord client
    """
    def rpc_login(self: Self, debug: bool = False) -> None:
        self.sock_send(self.sock, 0, debug, self.LOGIN_DATA)

    """
        Function: rpc_logout(debug)
        Used to forcefully logout (destroy) connection between RPCPy and Discord
    """
    def rpc_logout(self: Self, debug: bool = False) -> None:
        self.sock_send(self.sock, 0, debug, self.LOGOUT_DATA)

    """
        Function: rpc_update(debug)
        Used to update Discord RPC
    """
    def rpc_update(self: Self, debug: bool = False) -> None:
        self.sock_send(self.sock, 1, debug, self.RPC_OBJ)

