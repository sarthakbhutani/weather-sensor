import asyncpg
from fastapi import FastAPI
from fastapi import FastAPI, Request, Response
import logging
from app.routes import sensor_routes as sensor_route_file
import traceback
from app.settings import (DB_USERNAME,
DB_PASSWORD,
DB_NAME,
DB_HOST,LOG_LEVEL,SERVICE_NAME,
BASE_ROUTE,
DB_PORT)
import os
from app.dependencies import get_pool

app = FastAPI()

@app.on_event("startup")
async def startup():
    setup_logger(app)
    setup_routes(app)
    # await setup_db(app)
    app.state.db = await get_pool()

@app.on_event("shutdown")
async def shutdown():
    print("SHUTDOWN BABY------------------------------")
    await app.state.db.close()

import time


#set request data again
async def set_body(request: Request, body: bytes):
    async def receive():
        return {'type': 'http.request', 'body': body}
    request._receive = receive


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     # getting request body to log in case of failure
#     request_body = await request.body()
#     #setting again request body in request as it can be read once during a request session 
#     await set_body(request , request_body)
#     # response = await call_next(app,request)
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response


def setup_logger(app):
    """Set up the logger."""
    extra = {"app_name": SERVICE_NAME}
    logging.basicConfig(level=logging.INFO, format=f"%(asctime)s {SERVICE_NAME} %(message)s", force=True)
    logger = logging.getLogger(__name__)
    logger = logging.LoggerAdapter(logger, extra)
    logger.setLevel(logging.getLevelName(LOG_LEVEL))
    app.logger = logger
    app.state.logger = logger


def setup_routes(app):
    """Register routes."""
    app.logger.info('setup_routes')
    routes = [sensor_route_file]
    for route in routes:
        app.include_router(route.router, tags=["atlys"], prefix=f"{BASE_ROUTE}")


async def setup_db(app):
    """Set up db"""
    app.logger.info('setup_db')
    # try:
    #     import pdb
    #     pdb.set_trace()
    #     app.db = await asyncpg.connect(user=DB_USERNAME, password=DB_PASSWORD, database=DB_NAME, host=DB_HOST,port=DB_PORT)
    #     result = await app.db.fetch('SELECT * FROM mytable')
    #     print(result)
    # except Exception as e:
    #     app.logger.error(f"setup_db | error - {str(e)} | traceback - traceback - {traceback.format_exc()}")
    #     raise e


# async def get_data_from_database():
    # conn = await asyncpg.connect(user=DB_USERNAME, password=DB_PASSWORD, database=DB_NAME, host=DB_HOST)
    # result = await conn.fetch('SELECT * FROM mytable')
    # await conn.close()
    # return result 