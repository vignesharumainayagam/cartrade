from __future__ import unicode_literals

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
	path = frappe.local.request.path
	context.path = path
	word = path.split('-')
	Category=frappe.db.get_all('Category', 
								fields=['category_name','route','name'],
							    filters={'route':word[1].replace("/", "")})

	Brand=frappe.db.get_all('ItemBrand', 
							 fields=['route','name','brand_name','meta_title','meta_description','meta_keywords'],
							 filters={'route':word[0].replace("/", "")})

	ItemList=frappe.db.get_all('Item', 
								fields=['item_name','category','csd_rate','market_rate','route',
										'featured_image','short_description','brand'],
								filters={'brand':Brand[0].name,'category':Category[0].name},
								order_by= "name",limit_page_length=20)

	
	for Recentitem in ItemList:
		ItemBrand=frappe.db.get_all('ItemBrand', fields=['route','name','brand_name'],filters={'name':Recentitem.brand})
		ItemCategory=frappe.db.get_all('Category', fields=['route','name','category_name'],filters={'name':Recentitem.category})
		Recentitem.BrandUrl=ItemBrand[0].route
		Recentitem.CategoryUrl=ItemCategory[0].route
	context.Category=Category
	context.ItemList=ItemList
	context.Brand=Brand
	if Item[0].meta_title:
		context.title=Brand[0].brand_name
	if Item[0].meta_title != None:
		context.title=Brand[0].meta_title


	context.MetaDescription=Brand[0].meta_description
	context.MetaKeywords=Brand[0].meta_keywords
	context.CurrentUrl=frappe.utils.get_url()+path



