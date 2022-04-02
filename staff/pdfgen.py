from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template


def get_pdf_from_template(template, content_dict = {}):
    template = get_template(template)
    html = template.render(content_dict)
    results = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), results)
    if not pdf.err:
        return HttpResponse(results.getvalue(), content_type="application/pdf")
    return None