app_name = "college_custom"
app_title = "my custom app"
app_publisher = "pavithran"
app_description = "Custom college management features"
app_email = "pavithran.profession@gmail.com"
app_license = "mit"
add_to_apps_screen = [
    {
        "name": "college_custom",
        "logo": "/assets/college_custom/images/college-custom-logo.svg",
        "title": "my custom app",
        "route": "/desk"
    }
]
# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "college_custom",
# 		"logo": "/assets/college_custom/logo.png",
# 		"title": "my custom app",
# 		"route": "/college_custom",
# 		"has_permission": "college_custom.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/college_custom/css/college_custom.css"
# app_include_js = "/assets/college_custom/js/college_custom.js"

# include js, css files in header of web template
# web_include_css = "/assets/college_custom/css/college_custom.css"
# web_include_js = "/assets/college_custom/js/college_custom.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "college_custom/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_js = {
	"Gate Pass": "gateflow/doctype/gate_pass/gate_pass.js"
}

# Installation
# ------------

# before_install = "college_custom.install.before_install"
after_install = "college_custom.setup.after_install"
after_migrate = "college_custom.setup.after_migrate"

# Scheduled Tasks
# ---------------

scheduler_events = {
	"hourly": [
		"college_custom.gateflow.tasks.check_expired_passes"
	],
}


# Testing
# -------

# before_tests = "college_custom.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "college_custom.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "college_custom.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "college_custom.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["college_custom.utils.before_request"]
# after_request = ["college_custom.utils.after_request"]

# Job Events
# ----------
# before_job = ["college_custom.utils.before_job"]
# after_job = ["college_custom.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"college_custom.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

