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
@File       : video.py

@Author     : hsn

@Date       : 2024/8/14 下午3:52
"""
import uuid
from datetime import datetime
from pathlib import Path

import ffmpeg
from pywebio import pin
from pywebio.output import put_markdown, put_buttons, put_text, use_scope, put_row, put_button, \
    remove, put_scope, toast
from pywebio.pin import put_input, put_select, put_file_upload

from src.task.task_manager import tm
from src.task.tasks.video_convert import VideoConvertTask
from src.webio.page_templet import PageTemplet


class VideoConversion(PageTemplet):
    def __init__(self):
        super().__init__()
        self.creating_task = False

    def _on_unload(self):
        pass

    def _on_register(self):
        pass

    def _on_load(self):
        with use_scope(self.uuid):
            put_markdown("## Video Conversion")
            put_buttons(['to mp4', 'to mkv'], onclick=self._on_create_task)

    def _on_create_task(self, method: str):
        if self.creating_task:
            toast('Please close the current task first.')
            return
        self.creating_task = True
        self.__getattribute__(f'{method.replace(" ", "_")}')()

    def to_mp4(self):
        def start(output_format: str, _middlewares: list, files: list):
            if not files:
                toast('Please upload a video file first.')
                return
            if not output_format:
                output_format = '{name}.mp4'
            if not output_format.endswith('.mp4'):
                toast('The output format must be mp4.')
                return

            # cache the video file
            (p := Path("temp")).mkdir(exist_ok=True)
            file_index: [str, str] = {}
            for file in files:
                uid = uuid.uuid4().hex
                file_index[file['filename']] = uid
                with open(p / uid, 'wb') as f:
                    f.write(file['content'])
            # convert the video file
            for file_name, uid in file_index.items():
                input_file = p / uid
                output_file = p / output_format.format(name=file_name.split(".")[0],
                                                       name_with_prefix=file_name,
                                                       date=datetime.now().strftime("%Y-%m-%d"),
                                                       time=datetime.now().strftime("%H-%M-%S"))

                options = {}
                for middleware in _middlewares:
                    if middleware['name'] == 'Resolution':
                        options['vf'] = f'scale={pin.pin[middleware["input_uuid"]]}'
                    elif middleware['name'] == 'Bitrate':
                        options['b:v'] = middleware['input']
                print(options)

                tm.create_task(VideoConvertTask(input_file.as_posix(), (p/f"{uuid.uuid4().hex}.mp4").as_posix(), **options))
                # download the video file
                # with output_file.open( 'rb') as f:
                #     put_file(output_file.name, f.read())
                # download(file_name, f.read())

        create_task_uuid = uuid.uuid4().hex
        put_scope(create_task_uuid, scope=self.uuid)
        with use_scope(create_task_uuid):
            put_markdown('## Create Task')

            def _on_button_click(method: str):
                match method:
                    case 'start':
                        start(pin.pin[out_format_uuid], middlewares, pin.pin[put_file_upload_uuid])
                    case 'cancel':
                        remove(create_task_uuid)

            put_buttons(['start', 'cancel'], onclick=_on_button_click, small=True)
            put_file_upload_uuid = uuid.uuid4().hex
            put_file_upload(put_file_upload_uuid,
                            accept='.mp4,.mkv',
                            help_text='Upload the video file you want to convert',
                            multiple=True
                            )
            out_format_uuid = uuid.uuid4().hex
            put_input(name=out_format_uuid, label='Output format:', placeholder='{name}.mp4')
            put_markdown("""<font size=1>'{name_with_prefix}': the name of the video with the prefix of the video format.
'{name}': the name of the video without the prefix of the video format.
'{date}': the current date.
'{time}': the current time. </font>
            """)

            put_markdown('### Middlewares')
            middleware_select_uuid = uuid.uuid4().hex
            middlewares = []

            def add_middleware(name: str):
                middleware_uuid = uuid.uuid4().hex
                input_uuid = uuid.uuid4().hex

                put_scope(middleware_uuid, scope=create_task_uuid)
                with use_scope(middleware_uuid):
                    put_row([
                        put_text(f"{name}: "),
                        put_input(input_uuid, placeholder='value'),
                        put_button('Remove', onclick=lambda: remove_middleware(middleware_uuid))
                    ])
                middlewares.append({
                    'uuid': middleware_uuid,
                    'name': name,
                    'input_uuid': input_uuid,
                    'input': pin.pin[input_uuid]
                })

            def remove_middleware(middleware_uuid):
                middlewares.remove(next(filter(lambda m: m['uuid'] == middleware_uuid, middlewares)))
                remove(middleware_uuid)

            put_row([
                put_select(middleware_select_uuid, options=[
                    "Resolution",
                    "Bitrate",
                ]),
                put_button('Add', onclick=lambda: add_middleware(pin.pin[middleware_select_uuid]))
            ])
            put_markdown("---")

    def to_mkv(self):
        put_text('Converting to mkv')
