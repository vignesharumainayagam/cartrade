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
import frappe.utils
from frappe.utils import cint, cstr
import frappe.model.meta
import frappe.defaults
import frappe.translate
from frappe.utils.change_log import get_change_log
from six.moves.urllib.parse import unquote
from six import text_type



def get_context(context):
	path = frappe.local.request.path
	path = path.replace("/", "")
	context.path = path

	location = frappe.request.cookies.get('location')

	LatestNews=frappe.db.get_all('News', fields=['title','description','image','category','route'],limit_page_length=6)
	


	

	pathcategory = frappe.db.get_list('Category', fields=['name','route'], filters={'route':path.lower()})	
	pathcategoryname = pathcategory[0].name
	
	if pathcategoryname.endswith('s'):
		context.pathcategory = pathcategory[0].name[:-1]

	else:
		context.pathcategory = 	pathcategoryname


	items=frappe.db.get_all('Item', fields=['route','item_name','brand', 'category'], filters={'category'.lower():pathcategoryname} ,limit_page_length=10)

	context.items = items


	context.banner_image = frappe.db.get_value('Category',
						  fieldname=['banner_image'], filters={'route':path.lower()})

	Brands=frappe.db.get_all('ItemBrand', 
		fields=['route','name','brand_name', 'category'], 
		filters={'category'.lower():pathcategoryname},
		limit_page_length=200)	
	for x in Brands:
		item_count = frappe.db.get_all("Item", fields=['name'], filters={'brand': x.name})
		x.count = len(item_count)	


	
	featured_products=frappe.db.get_all('Item', 
						fields=['item_name','brand','csd_rate','short_description', 'featured_image','route', 'category'], 
						filters={'is_featured': "yes", 'category': path},limit_page_length=6)
	for Recentitem in featured_products:
		ItemBrand=frappe.db.get_all('ItemBrand', fields=['route','name','brand_name'],filters={'name':Recentitem.brand})
		ItemCategory=frappe.db.get_all('Category', fields=['route','name','category_name'],filters={'name':Recentitem.category})
		Recentitem.BrandUrl=ItemBrand[0].route
		Recentitem.CategoryUrl=ItemCategory[0].route

    
	context.featured_products = featured_products
	context.LatestNews = LatestNews
	context.Brands = Brands


	

