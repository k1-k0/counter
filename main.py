from aiohttp import web

from basic_handlers import basic_routes


def make_app():
    app = web.Application()
    app.router.add_routes(basic_routes)
    app.router.add_static('/', './static')
    return app

if __name__ == '__main__':
    web.run_app(app=make_app())
