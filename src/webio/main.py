#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#  Copyright (C) 2024. Suto-Commune
#  _
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  _
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#  _
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
@File       : main.py

@Author     : hsn

@Date       : 2024/8/14 下午2:30
"""
import pywebio.session
from pywebio.output import put_buttons, put_markdown

from src.webio.page_manager import PageManager
from .pages.home import HomePage
from .pages.video import VideoConversion
from .pages.progress import Progress
from ..config import config


class WebIO:
    def __init__(self):
        self.page_manager = PageManager()

    def start(self):
        import webview
        from pywebio.platform.flask import webio_view
        from flask import Flask

        app = Flask(__name__)

        # `task_func` is PyWebIO task function
        app.add_url_rule('/', 'webio_view', webio_view(self._start),
                         methods=['GET', 'POST', 'OPTIONS'])  # need GET,POST and OPTIONS methods
        if config.get("mode",None)=="Client":
            webview.create_window("TransFile", app, width=1000, height=800)
            webview.start()
        elif config.get("mode",None)=="Server":
            app.run("localhost", 8080)

    def _start(self):
        pywebio.session.set_env(output_animation=False)
        self.page_manager.register(HomePage())
        self.page_manager.register(VideoConversion())
        self.page_manager.register(Progress())
        # put_markdown("# Welcome")
        put_buttons(list(filter(lambda s: not s.startswith("_"), self.page_manager.page_name_map.keys())),
                    onclick=self.load)
        put_markdown("---")
        self.load("HomePage")

    def load(self, page_name: str):
        self.page_manager.load(self.page_manager.page_name_map[page_name])
