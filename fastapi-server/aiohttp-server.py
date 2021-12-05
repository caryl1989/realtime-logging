import asyncio
import json
from datetime import datetime
from aiohttp import web
from aiohttp.web import Application, Response
from aiohttp_sse import sse_response


async def hello(request):
    async with sse_response(request) as resp:
        while True:
            time_dict = {"time": f"Server Time : {datetime.now()}"}
            data = json.dumps(time_dict, indent=2)
            # print(data)
            await resp.send(data)
            await asyncio.sleep(1)


async def startLogging(request):
    app = request.app
    data = await request.post()

    payload = json.dumps(dict(data))
    print(payload)
    return Response()


async def index(request):
    d = """
        <html>
        <head>
            <style>
              #response {
                background-color: black;
                color:white;
                height:600px;
                overflow-x: hidden;
                overflow-y: auto;
                text-align: left;
                padding-left:10px;
              }
              
            .button {
                background-color: #4CAF50; /* Green */
                border: none;
                color: white;
                padding: 16px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                -webkit-transition-duration: 0.4s; /* Safari */
                transition-duration: 0.4s;
                cursor: pointer;
            }

            .button1 {background-color: #4CAF50;}
            .button2 {background-color: #f44336;}
            .button3 {background-color: #008CBA;}
      
            </style>
            <script type="text/javascript"
                src="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.8.0.js"></script>
            <script type="text/javascript">
                $(document).ready(function(){
                    var evtSource = new EventSource("/hello");
                    
                    $('#startLogging').click(function(){
                        evtSource.onmessage = function(e) {
                          $('#response').append(e.data + "<br>");
                        }
                        console.log("hahahahah");
                        $.post('/startLogging',
                        {
                          sender: "cary",
                          message: "how are you"
                        })
                    });
                });
            </script>
        </head>
        <body>
            <h1>Response from server:</h1>
            <div id="response"></div>
            <button class="button button1" id="startLogging">Start</button>
            <button class="button button2" id="stopLogging">Stop</button>
            <button class="button button3" id="downloadBlf">Download</button>
        </body>
    </html>
    """
    return web.Response(text=d, content_type="text/html")


if __name__ == "__main__":
    app = web.Application()
    app.router.add_route("GET", "/hello", hello)
    app.router.add_route("GET", "/index", index)
    app.router.add_route("POST", "/startLogging", startLogging)
    web.run_app(app, host="127.0.0.1", port=8080)