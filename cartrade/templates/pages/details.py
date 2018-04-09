# -*- coding: utf-8 -*-
# Copyright (c) 2018, Tridots Tech Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
# from _future_ import unicode_literals
import frappe
import frappe.utils
from frappe.utils.oauth import get_oauth2_authorize_url, get_oauth_keys, login_via_oauth2, login_via_oauth2_id_token, login_oauth_user as _login_oauth_user, redirect_post_login
import json
from frappe import _
from frappe.auth import LoginManager
from frappe.integrations.doctype.ldap_settings.ldap_settings import get_ldap_settings
from frappe.utils.password import get_decrypted_password
from frappe.utils.html_utils import get_icon_html



def get_context(context):
	location = frappe.request.cookies.get('city_location')

	path = frappe.local.request.path
	context.path = path
	word = path.split('/')

	item_route= word[2].lower()


	brand_route = word[1].split("-")[0]
	category_route = word[1].split("-")[1]

	context.category_route = category_route
	context.brand_route = brand_route

	brand_name = frappe.db.get_value("ItemBrand", 
						 filters={'route': brand_route}, fieldname=['name'])

	item = frappe.db.get_all('Item', 
				   fields=['route','item_name', 'brand', 'csd_rate', 'short_description', 'featured_image', 'name'],
				   filters={'route'.lower(): item_route, 'brand': brand_name},
				   limit_page_length=1)

	context.item_route = item_route

	context.item_brand = frappe.db.get_value("ItemBrand", 
						 filters={'name'.lower(): item[0].brand}, fieldname=['brand_name'])
	context.item_name = item[0].item_name
	context.base_price = item[0].csd_rate
	context.featured_image = item[0].featured_image
	context.short_description = item[0].short_description
	

	context.locations = frappe.db.get_all("City",
						fields=['name','city_name'],
						limit_page_length= 100)

	item_variants = frappe.db.get_all("Item Variant",
					fields=['route','variant_name', 'brand', 'item', 'name'],
				    filters={'item': item[0].name},
				    limit_page_length= 100)


	for x in item_variants:
		x.variant_price_for_delhi = frappe.db.get_value('Item Variant Price', 
									  fieldname=['price'], 
									  filters={'variant': x.name, 'city': 'Delhi'}
									  )

		x.variant_price_for_selected_city = frappe.db.get_value('Item Variant Price', 
										  	fieldname=['price'], 
										  	filters={'variant': x.name, 'city': 'selected_ity'}
										  	)	




	context.item_variants = item_variants	

	context.dealers_in_delhi = frappe.db.get_all("Dealers",
								fields=['dealer_name','dealer_address', 'dealer_phone', 'route'],
							    filters={'city': "Delhi", "brand": item[0].brand},
							    limit_page_length= 10)	

	context.dealers_in_selected_city = frappe.db.get_all("Dealers",
								fields=['dealer_name','dealer_address', 'dealer_phone', 'route'],
							    filters={'city': location, "brand": item[0].brand},
							    limit_page_length= 10)




	












