from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema
from accounts.repos import AccountRepository
from products.repos import CourseRepository
from deals.repos import DealRepository
from contracts.repos import ContractRepository
from .services import AnalyticsService

def get_analytics_service():
    return AnalyticsService(
        acc_repo=AccountRepository,
        course_repo=CourseRepository,
        deal_repo=DealRepository,
        contract_repo=ContractRepository,
    )

@extend_schema(tags=['v1_analytics'])
@api_view(["GET"])
def lead_customer_conv_rate(request):
    service = get_analytics_service()
    return Response(data={"lead_customer_conversion_rate": service.lead_customer_conv_rate()}, status=status.HTTP_200_OK) #setup response schema later

@extend_schema(tags=['v1_analytics'])
@api_view(["GET"])
def deal_won_conv_rate(request):
    service = get_analytics_service()
    return Response(data={"deal_won_conversion_rate": service.deal_won_conv_rate()},status=status.HTTP_200_OK) # to much duplications

@extend_schema(tags=['v1_analytics'])
@api_view(["GET"])
def total_pipeline_value(request):
    return Response(data={"total_pipeline_value": get_analytics_service().total_pipeline_value()}, status=status.HTTP_200_OK)

@extend_schema(tags=['v1_analytics'])
@api_view(["GET"])
def total_revenue(request):
    return Response(data={"total_revenue": get_analytics_service().total_revenue()}, status=status.HTTP_200_OK)

@extend_schema(tags=['v1_analytics'])
@api_view(["GET"])
def new_revenue(request):
    return Response(data={"new_revenue": get_analytics_service().new_revenue()}, status=status.HTTP_200_OK)

@extend_schema(tags=['v1_analytics'])
@api_view(["GET"])
def popular_courses(request):
    # n = int(request.query_params.get("n", 3)) # list of 3 by default in service #!!
    return Response(data={"popular_courses": get_analytics_service().popular_courses()}, status=status.HTTP_200_OK)

@extend_schema(tags=['v1_analytics'])
@api_view(["GET"])
def summary(request):
    service = get_analytics_service()
    return Response(
        data={
            "lead_customer_conversion_rate": service.lead_customer_conv_rate(),
            "deal_won_conversion_rate": service.deal_won_conv_rate(),
            "total_pipeline_value": service.total_pipeline_value(),
            "total_revenue": service.total_revenue(),
            "new_revenue": service.new_revenue(),
            "popular_courses": service.popular_courses(),
        }, status=status.HTTP_200_OK
    )