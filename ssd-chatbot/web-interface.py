import http.server
import socketserver
import asyncio
import websockets
import threading
from main import AbstractUserInterface, InitialChatbotState

HOMEPAGE_PORT = 80
WEBSOCK_PORT = 8081


class WebInterface(AbstractUserInterface):
    def __init__(self, websocket):
        super().__init__(InitialChatbotState())
        self.websocket = websocket
        self.event_loop = asyncio.get_event_loop()
        self.future = None

    def print(self, message):
        self.future = asyncio.run_coroutine_threadsafe(self.websocket.send(message), self.event_loop)
        return self.future.result()

    def input(self) -> str:
        self.future = asyncio.run_coroutine_threadsafe(self.websocket.recv(), self.event_loop)
        return self.future.result()

    def start(self):
        s = super().start

        def user_thread():
            nonlocal s
            try:
                s()
            finally:
                print("Exiting thread")

        t = threading.Thread(target=user_thread)
        t.start()

    def stop(self):
        if self.future:
            try:
                self.future.cancel()
            except:
                pass


def start_homepage_server():
    """Host static files at http://localhost:80"""
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory='static', **kwargs)
    with socketserver.TCPServer(("", HOMEPAGE_PORT), Handler) as httpd:
        httpd.serve_forever()


async def websock_handler(websocket):
    """Handle one connection"""
    ui = WebInterface(websocket)
    ui.start()
    try:
        await websocket.wait_closed()
    finally:
        ui.stop()


async def start_websock_server():
    """Handle all connections"""
    async with websockets.serve(websock_handler, '', WEBSOCK_PORT):
        await asyncio.Future()

# start both threads
homepage_thread = threading.Thread(target=start_homepage_server)
homepage_thread.start()
asyncio.run(start_websock_server())
homepage_thread.join()
