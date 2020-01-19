from flask import render_template, redirect
from flask_bootstrap import Bootstrap


class AppInitializer(object):
    """
    这个类, 是在app.py中创建 app 对象后, 初始化一些必要的内容, 比如初始化支持的url, 初始化 BootStrap 等等.
    """
    @classmethod
    def route(cls, app):
        @app.route("/")
        def home():
            return render_template("home.html")

        @app.route("/baidu")
        def baidu():
            target_url = "https://baidu.com"
            return redirect(target_url)

        @app.route("/daily_report")
        def daily_report():
            return render_template("daily_report.html")

    @classmethod
    def bootstrap(cls, app):
        return Bootstrap(app)

    @classmethod
    def error(cls, app):
        @app.errorhandler(404)
        def page_not_found(e):
            return render_template('404.html'), 404

        @app.errorhandler(500)
        def internal_server_error(e):
            return render_template("internal_server_error.html"), 500