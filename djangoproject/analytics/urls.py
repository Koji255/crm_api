from django.urls import path
from . import views

urlpatterns = [
    path("from-lead-to-customer-conversion-rate/", views.lead_customer_conv_rate),
    path("from-deal-to-won-conversion-rate/", views.deal_won_conv_rate),
    path("total-pipeline-value/", views.total_pipeline_value),
    path("total-revenue/", views.total_revenue),
    path("last-month-revenue/", views.new_revenue),
    path("popular-courses/", views.popular_courses),
    path("summary/", views.summary),
]