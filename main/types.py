from pyrogram.raw.types import KeyboardButtonRequestPeer

class ButtonRequestPeer:
    def __init__(self, text, button_id, peer_type, max_quantity=1):
        self.text = text
        self.button_id = button_id
        self.peer_type = peer_type
        self.max_quantity = max_quantity

    def write(self):
        return KeyboardButtonRequestPeer(
            text=self.text, button_id=self.button_id, peer_type=self.peer_type, max_quantity=self.max_quantity
        )
