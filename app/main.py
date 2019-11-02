from aiohttp import web
import app.routes as routes

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Helloooo, " + name
    return web.Response(text=text)

app = web.Application()
routes.setup_routes(app)

if __name__ == '__main__':
    web.run_app(app)