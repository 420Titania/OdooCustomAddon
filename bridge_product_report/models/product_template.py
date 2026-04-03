from odoo import models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    def action_print_product_pdf(self):
        return self.env.ref(
            "bridge_product_report.action_product_report"
        ).report_action(self)
