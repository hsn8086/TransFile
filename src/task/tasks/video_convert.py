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
@File       : video_convert.py

@Author     : hsn

@Date       : 2024/8/14 下午8:59
"""
import logging
import queue
import threading

import ffmpeg
from ffmpeg import run_async

from src.task.task_manager import Task


class VideoConvertTask(Task):
    def __init__(self, input_file, output_file, **kwargs):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.options = kwargs

    def _run(self):
        def reader(pipe, _queue):
            try:
                with pipe as p:
                    for _line in iter(p.readline, b''):
                        _queue.put(_line)
            finally:
                _queue.put(None)

        total_duration = ffmpeg.probe(self.input_file)['format']['duration']
        sepia_values = [.393, .769, .189, 0, .349, .686, .168, 0, .272, .534, .131]
        stream = (ffmpeg
                  .input(self.input_file)
                  #.colorchannelmixer(*sepia_values)
                  .output(self.output_file, **self.options)
                  .global_args('-progress', 'pipe:1')
                  .overwrite_output())
        logging.getLogger("VideoConvertTask").info(f'start with cmd:{stream.get_args()}')
        t = run_async(stream, pipe_stdout=True, pipe_stderr=True)
        q = queue.Queue()
        errors=queue.Queue()
        threading.Thread(target=reader, args=(t.stdout, q)).start()
        threading.Thread(target=reader, args=(t.stderr, errors)).start()
        print(total_duration)

        for line in iter(q.get, b''):
            if not line:
                break
            text: str = line.decode()
            text.rstrip()
            parts = text.split('=')
            key = parts[0] if len(parts) > 0 else ''
            value = parts[1] if len(parts) > 1 else ''
            if key == 'out_time_ms':
                try:
                    self.progress = float(value) / float(total_duration) / 1000000
                except ValueError:
                    ...
        error=""
        for line in iter(errors.get, b''):
            if not line:
                break
            error+=line.decode()
        self.status = 'done'
        self.error=error
        print('done')

    def _stop(self):
        pass

    def get_result(self):
        return self.output_file
