import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['code']
        self.group_name = f"room_{self.room_code}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # 🟢 Send "user joined" system message
        username = (
            self.scope["user"].username
            if self.scope["user"].is_authenticated
            else "Guest"
        )

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "system_message",
                "message": f"{username} joined the room",
            }
        )

    async def disconnect(self, close_code):
        # 🔴 Send "user left" system message
        username = (
            self.scope["user"].username
            if self.scope["user"].is_authenticated
            else "Guest"
        )

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "system_message",
                "message": f"{username} left the room",
            }
        )

        await self.channel_layer.group_discard(self.group_name, self.channel_name)


    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get("type", "chat")

        if message_type == "chat":
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat_message",
                    "message": data.get("message"),
                    "user": data.get("user", "Guest"),
                }
            )

        elif message_type == "video":
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "video_message",
                    "action": data.get("action"),
                    "time": data.get("time"),
                    "videoId": data.get("videoId")
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "chat",
            "message": event["message"],
            "user": event.get("user", "Guest")
        }))

    async def video_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "video",
            "action": event.get("action"),
            "time": event.get("time"),
            "videoId": event.get("videoId")
        }))

    async def system_message(self, event):
        # Send system message to WebSocket
        await self.send(text_data=json.dumps({
            "type": "system",
            "message": event["message"],
        }))

