from django.urls import path
from .views import admin_dashboard, export_admins_csv  # Import your view

urlpatterns = [
    path("dashboard/", admin_dashboard, name="admin_dashboard"),
    path("export-admins-csv/", export_admins_csv, name="export_admins_csv"),  # ✅ Add this
]
