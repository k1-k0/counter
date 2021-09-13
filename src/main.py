from aiohttp import web

from config import STATIC_FOLDER_PATH
from handlers.basic import basic_routes


def make_app():
    app = web.Application()
    app.router.add_routes(basic_routes)
    app.router.add_static('/', STATIC_FOLDER_PATH)
    return app

if __name__ == '__main__':
    web.run_app(app=make_app())
