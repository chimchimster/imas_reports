from api import ReportDocx, ReportPDF, DocxReportQueue


api_routes = (
    ('/docx-report', ReportDocx),
    ('/pdf-report', ReportPDF),
    ('/docx-report-queue', DocxReportQueue),
)
