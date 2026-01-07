# -*- coding: utf-8 -*-

from odoo import models, fields, api
from reportlab.graphics import barcode
from base64 import b64encode


class custom_invoice_report(models.AbstractModel):
	_name = 'report.custom_invoice_report.custom_invoice_report'
	_description = "Report"

	@api.model
	def _get_report_values(self, docids, data=None):
		records = self.env['account.move'].browse(docids)
		
		sale_order_data = {}
		
		for invoice in records:
			sale_orders = self.env['sale.order'].search([('invoice_ids', 'in', [invoice.id])])
			
			if not sale_orders and invoice.invoice_origin:
				sale_orders = self.env['sale.order'].search([('name', '=', invoice.invoice_origin)])
			
			sale_order_data[invoice.id] = [
				{
					'name': so.name,
					'date_order': so.date_order,
					'amount_total': so.amount_total,
				} for so in sale_orders
			]
		
		return {
			'doc_ids': docids,
			'doc_model': 'account.move',
			'docs': records,
			'data': data,
			'sale_order_data': sale_order_data,
		}