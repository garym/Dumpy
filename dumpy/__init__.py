#!/usr/bin/env python

# Copyright 2014 Gary Martin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time


def retry(ntimes, exceptions=None, timeout=0):
    """decorator for retrying a function a given number of times on
    exceptions"""
    if exceptions is None:
        exceptions = Exception
    elif isinstance(exceptions, list):
        exceptions = tuple(exceptions)

    def run(func):
        def f(*args, **kwargs):
            starttime = time.time()
            for i in range(ntimes):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if i == ntimes - 1:
                        raise
                    if timeout and time.time() - starttime > timeout:
                        raise
        return f
    return run
