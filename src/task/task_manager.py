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
@File       : task_manager.py

@Author     : hsn

@Date       : 2024/8/14 下午8:45
"""
import threading
import uuid
from abc import abstractmethod, ABCMeta


class Task(metaclass=ABCMeta):
    def __init__(self):
        self.task_id = uuid.uuid4()
        self.task_name = self.__class__.__name__
        self.status = 'init'
        self.progress = 0

    @abstractmethod
    def _run(self):
        pass

    @abstractmethod
    def _stop(self):
        pass

    def run(self):
        self.status = 'running'
        self._run()
        self.status = 'done'

    def stop(self):
        self._stop()
        self.status = 'stopped'


class TaskManager:
    def __init__(self):
        self.tasks = {}

    def create_task(self, task: Task):
        task_id = task.task_id
        self.tasks[task_id] = task
        threading.Thread(target=task.run).start()
        return task_id

    def get_tasks(self):
        return self.tasks


tm = TaskManager()
