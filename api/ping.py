from vibora import Vibora
from vibora.limits import RouteLimits
from vibora.blueprints import Blueprint
from vibora.responses import JsonResponse

router = Blueprint()

@router.route('/ping', methods=['GET'])
async def ping():
  return JsonResponse({'ping': 'pong'})