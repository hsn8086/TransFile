#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#  Copyright (C) 2023. HCAT-Project-Team
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

@Date       : 2024/5/6 下午12:10
"""
import subprocess

import eel
from pathlib import Path
import webview
@eel.expose
def say_hello_py(x):
    print(f'Hello from {x}!')
def main():
    subprocess.run(['npm', 'run', 'build'], cwd='trans-file-web')
    # eel.init(Path('web').as_posix())
    # eel.start('index.html', size=(320, 120), port=8080)
    webview.create_window('My first webview', 'web/index.html')
    webview.start()
