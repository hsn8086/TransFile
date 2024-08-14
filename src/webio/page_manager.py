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
@File       : page_manager.py

@Author     : hsn

@Date       : 2024/8/14 下午2:01
"""
from src.webio.page_templet import PageTemplet


class PageManager:
    def __init__(self):
        self.pages = {}
        self.active_page: PageTemplet = None
        self.page_name_map = {}

    def register(self, page: PageTemplet) -> None:
        self.pages[page.uuid] = page
        page.register()
        self.page_name_map[page.name] = page.uuid

    def load(self, page_uuid: str) -> None:
        if self.active_page:
            self.active_page.unload()

        self.active_page = self.pages.get(page_uuid)
        self.active_page.load()
