#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-31 01:01
# Author:  rongli
# Email:   abc@xyz.com
# File:    handlers.py
# Project: fa-demo
# IDE:     PyCharm
# -*- coding:utf-8 -*-
"""
@Created on : 2022/4/22 22:02
@Author: binkuolo
@Des: 异常处理
"""

from logging import getLogger
from typing import Union

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from tortoise.exceptions import DoesNotExist, IntegrityError, OperationalError, ValidationError as MysqlValidationError

from .exc import UnicornException

logger = getLogger('fastapi')


async def mysql_validation_error(_: Request, exc: MysqlValidationError):
    """     数据库字段验证错误    """
    logger.error(f"数据库字段验证错误  {str(exc)}")
    return JSONResponse({
        "code": -1,
        "msg": str(exc),
        "data": None
        }, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


async def mysql_integrity_error(_: Request, exc: IntegrityError):
    """    数据库完整性错误    """
    logger.error(f"数据库完整性错误  {exc}")
    return JSONResponse({
        "code": -1,
        "msg": str(exc),
        "data": None
        }, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


async def mysql_does_not_exist(_: Request, exc: DoesNotExist):
    """     mysql 查询对象不存在异常处理    """
    logger.error(f"数据库查询对象不存在异常处理 {str(exc)}")
    return JSONResponse({
        "code": -1,
        "msg": "发出的请求针对的是不存在的记录，服务器没有进行操作。",
        "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)


async def mysql_operational_error(_: Request, exc: OperationalError):
    """    mysql 数据库异常错误处理    """
    logger.error(f"数据库 OperationalError 异常 {str(exc)}")
    return JSONResponse({
        "code": -1,
        "msg": "数据操作失败",
        "data": None
        }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def http_error_handler(_: Request, exc: HTTPException):
    """    http异常处理    """
    logger.error(f"http异常处理 {exc.status_code=} {exc.detail=}")
    if exc.status_code == 401:
        return JSONResponse({
            "code": -1,
            "msg": exc.detail,
            "data": None
            }, status_code=status.HTTP_401_UNAUTHORIZED)

    return JSONResponse({
        "code": exc.status_code,
        "msg": exc.detail,
        "data": exc.detail
        }, status_code=exc.status_code, headers=exc.headers)


async def unicorn_exception_handler(_: Request, exc: UnicornException):
    """    unicorn 异常处理    """
    logger.error(f"unicorn 异常处理  {exc.code=}  {exc.errmsg=}  {exc.data=}")
    return JSONResponse({
        "code": exc.code,
        "msg": exc.errmsg,
        "data": exc.data,
        }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def http422_error_handler(_: Request, exc: Union[RequestValidationError, ValidationError], ) -> JSONResponse:
    """    参数校验错误处理    """
    logger.error(f"参数校验错误处理[422] {exc.errors()=}")
    return JSONResponse({
        "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "msg": f"数据校验错误",
        "data": exc.errors(),
        }, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, )
