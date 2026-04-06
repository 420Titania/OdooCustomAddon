import base64

from odoo import api, models
from odoo.modules.module import get_module_resource

class ProductReport(models.AbstractModel):
    _name = 'report.bridge_product_report.product_report_template'
    _description = 'Product PDF Report'

    @api.model
    def _get_logo_data(self):
        """Return (base64_string, mime_type) for module logo."""
        candidates = [
            ('logo.png', 'image/png'),
            ('logo.jpeg', 'image/jpeg'),
            ('logo.jpg', 'image/jpeg'),
        ]

        for filename, mime in candidates:
            logo_path = get_module_resource(
                'bridge_product_report', 'static', 'src', 'img', filename
            )
            if logo_path:
                with open(logo_path, 'rb') as logo_file:
                    return base64.b64encode(logo_file.read()).decode('ascii'), mime

        return '', 'image/png'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['product.template'].browse(docids)
        logo_base64, logo_mime = self._get_logo_data()
        return {
            'doc_ids': docids,
            'doc_model': 'product.template',
            'docs': docs,
            'logo_base64': logo_base64,
            'logo_mime': logo_mime,
        }
