# -*- coding: utf-8 -*-
# Copyright (c) 2018, Tridots Tech Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
# from _future_ import unicode_literals
import frappe
import frappe.utils
import json
from frappe import _


def get_context(context):
	path = frappe.local.request.path
	context.path = path
	word = path.split('/')

	brand_route = word[1].split("-")
	item_brand_route = brand_route[0].lower().replace("/", "")
	item_category_route = brand_route[1].lower().replace("/", "")
	


	context.item_brand_route = item_brand_route
	context.item_category_route = item_category_route

	item_route = word[2].lower().replace("/", "")

	context.item_route = item_route

	variant_route = word[3].lower().replace("/", "")
	item_name = frappe.db.get_value("Item", 
				filters={'route': item_route}, fieldname=['name'])

	
	context.item_brand = frappe.db.get_value("ItemBrand", 
						 filters={'route': item_brand_route}, fieldname=['brand_name'])

	context.item_title = frappe.db.get_value("Item", 
						 filters={'route': item_route}, fieldname=['item_name'])

	context.variant_title = frappe.db.get_value("Item Variant", 
						 filters={'route': variant_route}, fieldname=['variant_name'])

	

	context.item_featured_image = frappe.db.get_value("Item", 
				filters={'route': item_route}, fieldname=['featured_image'])

	
	item_variant_doc_name = frappe.db.get_value("Item Variant", 
				filters={'route': variant_route}, fieldname=['name'])

	context.item_variant_doc_name =item_variant_doc_name

	context.locations = frappe.db.get_all("City",
						fields=['name','city_name'],
						limit_page_length= 100)


	context.item_variants = frappe.db.get_all("Item Variant",
					fields=['route','variant_name', 'name'],
				    filters={'item': item_name},
				    limit_page_length= 100)

	context.variant = frappe.get_all('Item Variant',
					  fields=['length', 'wheelbase', 'width', 'ground_clearance', 'height', 'kerb_weight',
					  	      'doors', 'bootspace', 'seating_capacity', 'no_of_seating','fuel_tank',
					  	      'engine_type', 'mileage_arai', 'dual_clutch', 'cylinders', 'max_torque', 'transmission_type', 'engine_start',
					  	      'cylinder_configuration', 'turbocharger', 'sport_mode', 'fuel_type', 'turbocharger_type', 'manual_shifting',
					  	      'displacement', 'drivetrain', 'alternate_fuel', 'max_power', 'no_of_gears', 'driving_modes'], 
					  filters = {'route': variant_route, 'item': item_name})[0]

	context.item_variants_price_in_delhi = frappe.db.get_value("Item Variant Price", 
										   filters={'item': item_name, 'variant': item_variant_doc_name, 'city': 'Delhi'},
										   fieldname=['price'])

		    


	context.item_variants_price_in_current_city = frappe.db.get_value("Item Variant Price", 
										   filters={'item': item_name, 'variant': item_variant_doc_name, 'city': 'current_city'},
										   fieldname=['price'])