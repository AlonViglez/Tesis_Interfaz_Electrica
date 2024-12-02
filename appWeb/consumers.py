import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChartConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'grafica_pulso'

        # Unir al grupo de WebSocket
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print("Cliente conectado al WebSocket.")

    async def disconnect(self, close_code):
        # Eliminar del grupo de WebSocket
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("Cliente desconectado del WebSocket.")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')

        if action == 'pause':
            is_paused = text_data_json.get('isPaused', False)
            # Enviar el estado de pausa a todos los clientes
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'pause_update',
                    'isPaused': is_paused,
                }
            )

    async def pause_update(self, event):
        is_paused = event['isPaused']
        # Enviar el estado de pausa al cliente
        await self.send(text_data=json.dumps({
            'action': 'pause',
            'isPaused': is_paused
        }))

    async def send_data(self, data):
        # Enviar datos recibidos a todos los clientes conectados
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chart_data',
                'data': data
            }
        )

    async def chart_data(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))
