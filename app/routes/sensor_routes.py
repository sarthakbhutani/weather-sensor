from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from app.model.sensor_model import SensorRequestData
from app.dependencies import get_pool
from fastapi import FastAPI, Request
router = APIRouter()
import traceback

import json
async def common(request: Request):
    return (request.app.state.db,request.app.state.logger)


@router.get('/health')
async def health():
    return JSONResponse(status_code=200, content={"status":"ok"})

@router.post('/send-data')
async def __send_data(data : SensorRequestData, ass = Depends(common)):
    pool = ass[0]
    logger = ass[1]
    logger.info('__send_data',data)
    print(data)
    success = None
    try:
        async with pool.acquire() as conn:
            db_result = await conn.execute(f'insert into sensor_data(sensor_id,pm2,pm10,tvoc,hcho,temp,humidity,co2) values( {data.data.id}, {data.data.pm2}, {data.data.pm10}, {data.data.tvoc}, {data.data.hcho}, {data.data.temp}, {data.data.humidity}, {data.data.co2} )')
            print(db_result)
            success= True
    except Exception as e:
        logger.error(f'exception.__send_data : {data} | error - {str(e)} | traceback - traceback - {traceback.format_exc()}')
        success= False
    
    respose_dict = {
        "success": success,
    }
    if success:
        http_status_code = 200
    else:
        http_status_code = 500
    return JSONResponse(status_code=http_status_code, content=respose_dict)


@router.get('/get-indoor-data')
async def __get_data(ass = Depends(common)):
    pool = ass[0]
    logger = ass[1]
    logger.info('__get_data')
    success = None
    try:
        async with pool.acquire() as conn:
            records = await conn.fetchrow(f'select sensor_id,pm2,pm10,tvoc,hcho,temp,humidity,co2 from sensor_data order by id desc limit 1;')
            result = {}
            for k,v in records.items():
                result[k] = v
            success = True
    except Exception as e:
        logger.error(f'exception.__get_data | error - {str(e)} | traceback - traceback - {traceback.format_exc()}')
        success= False
    
    respose_dict = {
        "success": success,
        "data":result,
    }
    if success:
        http_status_code = 200
    else:
        http_status_code = 500
    return JSONResponse(status_code=http_status_code, content=respose_dict)


# POC CODE --------------
from datetime import datetime
import time
import asyncio
@router.get('/time-api-1')
async def time_api_1():
    start = datetime.now()
    print(f"/time-api-1 : request_received {start}")
    # time.sleep(20)
    for i in range(20):
        time.sleep(1)
    end = datetime.now()
    print(f"/time-api-1 : serving_response {end} || {end-start}")
    return {"ass":True}


@router.get('/time-api-11')
async def time_api_1():
    start = datetime.now()
    print(f"/time-api-11 : request_received {start}")
    # time.sleep(30)
    for i in range(30):
        time.sleep(1)
    end = datetime.now()
    print(f"/time-api-11 : serving_response {end} || {end-start}")
    return {"ass":True}


@router.get('/time-api-async')
async def time_api_2():
    start = datetime.now()
    print(f"/time-api-async : request_received {start}")
    await asyncio.sleep(10)
    end = datetime.now()
    print(f"/time-api-async : serving_response {end} || {end-start}")
    return {"ass":True}