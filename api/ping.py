from aiohttp import web

router = web.RouteTableDef()

@router.get('/healthz')
async def ping(request: web.Request):
  return web.json_response({'status': 'running'})
