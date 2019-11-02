from aiohttp import web
import app.routes as routes

app = web.Application()
routes.setup_routes(app)

if __name__ == '__main__':
    web.run_app(app)