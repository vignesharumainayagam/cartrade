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
	location = frappe.request.cookies.get('location')

	RecentProducts=frappe.db.get_all('Item', 
		fields=['item_name','category','csd_rate','market_rate','route','featured_image','short_description','brand'],
		limit_page_length=15)
	LatestNews=frappe.db.get_all('News', fields=['title','description','image','category'],limit_page_length=6)
	Categories=frappe.db.get_all('Category', fields=['category_name','route','name'],filters={'published':1})
	
	Brand=frappe.db.get_all('ItemBrand', fields=['route','name','brand_name', 'category'],filters={"category":("in", ['bikes', 'Cars'])})
	Item=frappe.db.get_all('Item', fields=['route', 'category','name','item_name'],filters={"category":("in", ['bikes', 'Cars'])})

	for Recentitem in RecentProducts:
		ItemBrand=frappe.db.get_all('ItemBrand', fields=['route','name','brand_name'],filters={'name':Recentitem.brand})
		ItemCategory=frappe.db.get_all('Category', fields=['route','name','category_name'],filters={'name':Recentitem.category})
		Recentitem.brandname = ItemBrand[0].brand_name
		Recentitem.BrandUrl=ItemBrand[0].route
		Recentitem.CategoryUrl=ItemCategory[0].route



	for x in Categories:
		x.categorybrands=frappe.db.get_list('ItemBrand', 
			fields=['brand_name','route','name'],
			filters={'category':x.name},
			limit_page_length=150)
		for y in x.categorybrands:
			item_count = frappe.db.get_all("Item", fields=['name'], filters={'brand': y.name})
			y.count = len(item_count)		

	context.brand= Brand	
	context.item = Item
	context.LatestNews = LatestNews
	context.RecentProducts = RecentProducts
	context.Categories = Categories

