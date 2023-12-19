from typing import Final

from api import ReportQueue

API_ROUTE: Final = '/api/v1/'

api_routes = (
    (API_ROUTE + 'get-report/', ReportQueue),
)
