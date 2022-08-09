#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-27 23:17
# Author:  rongli
# Email:   abc@xyz.com
# File:    cli_wraper.py
# Project: fa-demo
# IDE:     PyCharm
import asyncio
import functools
from typing import Callable, Coroutine

from tortoise import Tortoise

from ..config import settings


def _coro_wrapper(f: Callable[..., Coroutine]):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(f(*args, **kwargs))
        else:
            loop.run_until_complete(f(*args, **kwargs))

    return wrapper


def _tortoise_wrapper(f: Callable):
    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        await Tortoise.init(settings.tortoise_orm_config)
        try:
            await f(*args, **kwargs)
        finally:
            await Tortoise.close_connections()

    return wrapper


def cli_wrapper(f: Callable):
    return _coro_wrapper(_tortoise_wrapper(f))
