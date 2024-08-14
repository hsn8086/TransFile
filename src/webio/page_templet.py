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
@File       : page_templet.py

@Author     : hsn

@Date       : 2024/8/14 下午2:02
"""
import uuid
from abc import abstractmethod, ABCMeta

from pywebio.output import put_scope, remove


class PageTemplet(metaclass=ABCMeta):
    def __init__(self):
        self.uuid = uuid.uuid4().hex

    @property
    def name(self):
        return self.__class__.__name__

    def load(self):
        put_scope(name=self.uuid)
        self._on_load()

    @abstractmethod
    def _on_load(self):
        ...

    def unload(self):
        self._on_unload()
        remove(self.uuid)

    @abstractmethod
    def _on_unload(self):
        ...

    def register(self):
        self._on_register()

    @abstractmethod
    def _on_register(self):
        ...
