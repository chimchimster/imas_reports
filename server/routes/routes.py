import os
import sys

sys.path.append(
    os.path.join(
        os.getcwd().rstrip('reports')
    )
)

from typing import Final
from reports.server.api import ReportQueue
from reports.server.namespace.hook import SocketWebHookNamespace

API_ROUTE: Final = '/api/v1/'

api_routes = (
    (API_ROUTE + 'get-report/', ReportQueue),
)

SOCKET_ROUTE: Final = '/ws/'

socket_routes = (
    (SOCKET_ROUTE + 'get-report/', SocketWebHookNamespace),
)
