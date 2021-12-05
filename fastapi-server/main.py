from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
import uvicorn
from sh import tail
from fastapi.middleware.cors import CORSMiddleware
import time
import os
from aiohttp_sse import sse_response

# create our app instance
app = FastAPI()

# add CORS so our web page can connect to our api
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)
LOGFILE = f"{dir_path}/test.log"


# This async generator will listen to our log file in an infinite while loop (happens in the tail command)
# Anytime the generator detects a new line in the log file, it will yield it.
async def logGenerator(request):
    for line in tail("-f", LOGFILE, _iter=True):
        if await request.is_disconnected():
            print("client disconnected!!!")
            break
        yield line
        time.sleep(0.5)


# This is our api endpoint. When a client subscribes to this endpoint, they will receive SSE from our log file
'''
@app.get('/stream-logs')
async def run(request: Request):
    event_generator = logGenerator(request)
    return EventSourceResponse(event_generator)
'''


@app.get('/stream-logs')
async def run(request: Request):
    async with sse_response(request) as resp:
        for line in tail("-f", LOGFILE, _iter=True):
            if await request.is_disconnected():
                print("client disconnected!!!")
                break
        await resp.send(line)
        time.sleep(0.5)
    return resp


# run the app
uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
