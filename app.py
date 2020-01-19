from flask import Flask
from app_initializer import AppInitializer


app = Flask(__name__)
app.config.from_pyfile("./service.conf")

# 初始化所需的 route url
AppInitializer.route(app)

# 初始化 bootstrap
AppInitializer.bootstrap(app)

# 初始化 error handler
AppInitializer.error(app)