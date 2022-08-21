#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-27 23:19
# Author:  rongli
# Email:   abc@xyz.com
# File:    runserver.py
# Project: fa-demo
# IDE:     PyCharm
import os

import uvicorn
from starlette.routing import Mount
from typer import Typer

from ..config import settings
from ..models import Access
from ..server import app as fast_app
from ..utils import cli_wrapper

app = Typer()


@app.command(name='server', help='start uvicorn server')
def run_server(host: str = settings.server_host, port: int = settings.server_port):
    project_env = 'prod' if os.getenv('PROJECT_ENV') == 'prod' else 'dev'
    log_config_path = str(settings.base_dir / 'backend' / 'config' / f'logging.{project_env}.json')
    uvicorn.run(app='backend.server:app',
                host=host,
                port=port,
                reload=settings.debug,
                reload_dirs=["backend"],
                log_config=log_config_path)


@app.command(name='get_menulist', help='get_menulist')
@cli_wrapper
async def get_menulist():
    for router in fast_app.routes:
        if isinstance(router, Mount):
            continue
        if not router.include_in_schema:
            continue
        scopes = ""
        if router.dependencies:
            for d in router.dependencies:
                scopes = d.scopes[0]
                break
        if scopes:
            print(f"{router.name:>30}  {scopes:>30}  {router.summary}")
            access = await Access.get_or_none(scopes=scopes)
            path = router.path.replace(settings.url_prefix, '')
            if access is None:
                await Access.create(title=router.summary, scopes=scopes, path=path, name=router.name,
                                    access_desc=router.name)
            # else:
            #     await access.filter(scopes=scopes).update(title=router.summary, scopes=scopes, path=path,
            #                                               name=router.name,
            #                                               access_desc=router.name)
