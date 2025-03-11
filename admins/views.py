import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Admin

def admin_dashboard(request):
    search_query = request.GET.get("search", "")
    sort_by = request.GET.get("sort", "name")  # Default sorting by name
    order = request.GET.get("order", "asc")

    # Fetch and filter admins
    admins = Admin.objects.all()
    if search_query:
        admins = admins.filter(Q(name__icontains=search_query) | Q(email__icontains=search_query))

    # Sorting logic
    if order == "desc":
        sort_by = f"-{sort_by}"
    admins = admins.order_by(sort_by)

    # Pagination
    paginator = Paginator(admins, 10)
    page = request.GET.get("page")
    admins = paginator.get_page(page)

    return render(request, "admins/dashboard.html", {
        "admins": admins,
        "search_query": search_query,
        "sort_by": sort_by.strip("-"),
        "order": "desc" if order == "asc" else "asc"
    })

# Export CSV
def export_admins_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="admins.csv"'

    writer = csv.writer(response)
    writer.writerow(["Name", "Email", "Phone Number"])

    for admin in Admin.objects.all():
        writer.writerow([admin.name, admin.email, admin.phone_number])

    return response
