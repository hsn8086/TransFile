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
        self.task_id = uuid.uuid4().hex
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
        self.callback = {}
        self.groups = {}

    def create_task(self, task: Task, callback=None, label="main"):
        task_id = task.task_id
        self.tasks[task_id] = task
        if callback:
            self.callback[task_id] = callback
        if label not in self.groups:
            self.groups[label] = []
        self.groups[label].append(task_id)
        threading.Thread(target=self._start_task, args=(task.task_id,)).start()
        return task_id

    def _start_task(self, tid: str):
        task = self.tasks[tid]
        task.run()
        if tid in self.callback:
            self.callback[tid](task)
            self.callback.pop(tid)
        self.tasks.pop(tid)
        for label in self.groups:
            if tid in self.groups[label]:
                self.groups[label].remove(tid)

    def refresh(self):
        del_list = []
        for task in self.tasks.values():
            if task.status == 'done':
                if task.task_id in self.callback:
                    self.callback[task.task_id](self.tasks[task.task_id])
                del_list.append(task.task_id)
        for task_id in del_list:
            del self.tasks[task_id]

    def get_tasks(self, label=""):
        if label not in self.groups:
            return self.tasks.values()
        return [self.tasks[task_id] for task_id in self.groups[label]]

    def progress(self, label=""):
        if label not in self.groups:
            return (sum([task.progress for task in self.tasks.values()]) / len(self.tasks)) if len(
                self.tasks) != 0 else 1
        return (sum([self.tasks[task_id].progress for task_id in self.groups[label]]) / len(self.groups[label])) if len(
            self.groups[label]) != 0 else 1


tm = TaskManager()
