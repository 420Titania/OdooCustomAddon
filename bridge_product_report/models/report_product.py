import base64

from odoo import api, models
from odoo.modules.module import get_module_resource

class ProductReport(models.AbstractModel):
    _name = 'report.bridge_product_report.product_report_template'
    _description = 'Product PDF Report'

    @api.model
    def _get_status_summary(self, docs):
        summary = {
            'broken': 0,
            'rusak': 0,
            'dihibahkan': 0,
            'tidak_ada': 0,
        }

        for product in docs:
            status = (product.x_condition_status or '').strip().lower()
            if status == 'broken':
                summary['broken'] += 1
            elif status == 'rusak':
                summary['rusak'] += 1
            elif status == 'dihibahkan':
                summary['dihibahkan'] += 1
            elif status == 'tidak ada':
                summary['tidak_ada'] += 1

        return summary

    @api.model
    def _get_logo_data(self):
        """Return (base64_string, mime_type) for module logo."""
        preferred_logo = get_module_resource(
            'bridge_product_report', 'static', 'src', 'img', 'logo.png'
        )
        if preferred_logo:
            with open(preferred_logo, 'rb') as logo_file:
                return base64.b64encode(logo_file.read()).decode('ascii'), 'image/png'

        candidates = [
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
        web_base_url = (
            self.env['ir.config_parameter'].sudo().get_param('web.base.url', '')
        ).rstrip('/')
        status_summary = self._get_status_summary(docs)
        return {
            'doc_ids': docids,
            'doc_model': 'product.template',
            'docs': docs,
            'logo_base64': logo_base64,
            'logo_mime': logo_mime,
            'web_base_url': web_base_url,
            'status_summary': status_summary,
        }
