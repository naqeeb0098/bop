from . import __version__ as app_version

app_name = "bop"
app_title = "Bank of Punjab"
app_publisher = "Pukat Digital"
app_description = "App for the customizations required by Bank of Punjab"
app_email = "mavee.shah@hotmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/bop/css/bop.css"
# app_include_js = "/assets/bop/js/bop.js"

# include js, css files in header of web template
# web_include_css = "/assets/bop/css/bop.css"
# web_include_js = "/assets/bop/js/bop.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "bop/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "bop.utils.jinja_methods",
#	"filters": "bop.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "bop.install.before_install"
# after_install = "bop.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "bop.uninstall.before_uninstall"
# after_uninstall = "bop.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "bop.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

override_doctype_class = {
	"Employee": "bop.custom.custom_employee.customEmployee"
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
    "cron": {
		"10 0 * * *": [
			"bop.update_daily_markup"
		],
	"50 15 * * *":[
			"bop.bank_of_punjab.apis.loan.calculate_daily_markup"
		],
	"59 15 * * *":[
			"bop.bank_of_punjab.apis.cash_security.calculate_daily_markup_for_cash_security",
			"calculate_daily_provident_fund"
		]
	
	},
	"all": [
		"bop.tasks.all"
	],
	"daily": [
	 	"bop.tasks.daily"
	 ],
	# "hourly": [
	# 	"bop.tasks.hourly"
	# ],
	# "weekly": [
	# 	"bop.tasks.weekly"
	# ],
	# "monthly": [
	# 	"bop.tasks.monthly"
	# ],
}

# Testing
# -------

# before_tests = "bop.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "bop.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "bop.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["bop.utils.before_request"]
# after_request = ["bop.utils.after_request"]

# Job Events
# ----------
# before_job = ["bop.utils.before_job"]
# after_job = ["bop.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"bop.auth.validate"
# ]
fixtures = [
        {
        "dt": "Custom Field",
        "filters": [
            [
                "module", "in", [
                    "Bank of Punjab",
                ]
            ],
        ]

    },
    {
        "dt":"Server Script",
        "filters":[
            ["module","in",[
                "Bank of Punjab"
            ]]
        ]
    },
    {
        "dt":"Client Script",
        "filters":[
            ["module","in",[
                "Bank of Punjab"
            ]]
        ]
    }
]
