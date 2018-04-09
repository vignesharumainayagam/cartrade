# -*- coding: utf-8 -*-
# Copyright (c) 2018, Tridots Tech Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator

class Category(WebsiteGenerator):
	

	def validate(self):
		if ' ' in self.category_name:
			self.route = self.category_name.replace(" ", "").lower()