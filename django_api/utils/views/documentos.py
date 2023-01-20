import pdfkit

# Rest framework
from rest_framework.viewsets import GenericViewSet

# Django
from django.http.response import HttpResponse
from django.template.loader import get_template


class DocumentosView(GenericViewSet):

    options = {
        'page-size': 'Letter',
        'margin-top': '0.30in',
        'margin-right': '0.20in',
        'margin-bottom': '0.20in',
        'margin-left': '0.20in',
        'encoding': "UTF-8",
        # 'no-outline': None,
        "enable-local-file-access": True,
    }

    def generar_pdf(self, template, data, file_name='file', output_file=None):
        """
        Permite generar un archivo PDF
        """

        datos_template = {
            'data': data,
        }

        template = get_template(template)
        html = template.render(datos_template)

        pdf = pdfkit.from_string(html, output_file, options=self.options, css=[])

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + file_name + '.pdf"'

        return response