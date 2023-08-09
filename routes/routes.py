from api import ReportDocx, ReportPDF


api_routes = (
    ('/docx-report', ReportDocx),
    ('/pdf-report', ReportPDF),
)
