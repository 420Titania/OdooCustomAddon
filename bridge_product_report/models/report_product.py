from odoo import api, models

class ProductReport(models.AbstractModel):
    _name = 'report.bridge_product_report.product_report_template'
    _description = 'Product PDF Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['product.template'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'product.template',
            'docs': docs,
        }
