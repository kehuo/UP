from flask import Flask
from app_initializer import AppInitializer


app = Flask(__name__)
app.config.from_pyfile("./service.conf")

# 初始化所需的 route url / bootstrap / error handler
# AppInitializer.run_all(app)
