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
@File       : progress.py

@Author     : hsn

@Date       : 2024/8/14 下午8:58
"""
import threading
import time
import uuid

import pywebio.session
from pywebio.output import put_row, put_text, use_scope, put_markdown, put_scope, remove
from pywebio.session import register_thread

from ..page_templet import PageTemplet
from ...task.task_manager import tm


class Progress(PageTemplet):
    def __init__(self):
        super().__init__()
        self.loaded = False

    def _on_load(self):
        self.loaded = True
        with use_scope(self.uuid):
            put_markdown("## Progress")
            put_row([put_markdown('### Task Name'), put_markdown('### Status'), put_markdown('### Progress')])
        t = threading.Thread(target=self._event_loop)
        register_thread(t)
        t.start()

    def _event_loop(self):
        progress_uuid = uuid.uuid4().hex
        while self.loaded:
            remove(progress_uuid)
            put_scope(progress_uuid, scope=self.uuid)
            with use_scope(progress_uuid):
                put_row(
                    [put_markdown(f"**All**"), put_text(f"--"),
                     put_markdown(
                         f"**{tm.progress(pywebio.session.info.user_ip + pywebio.session.info.user_agent.ua_string)}**"
                     )
                     ]
                )
                for task in tm.get_tasks(pywebio.session.info.user_ip + pywebio.session.info.user_agent.ua_string):
                    put_row([put_text(task.task_name), put_text(task.status), put_text(str(task.progress))])
            time.sleep(1)

    def _on_unload(self):
        self.loaded = False

    def _on_register(self):
        pass
