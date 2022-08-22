from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

id_param = openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)


@api_view(['POST'])
def register(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response('ok')
    return Response(serializer.errors)

@api_view(['PUT'])
def profile_update(request):
    if request.user.is_authenticated:
        try:
            profile = Customer.objects.get(id=request.data['id'])
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.user == profile.user:
            serializer = CustomerSerializer(instance=profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response('ok')
            return Response(serializer.errors)
    return Response("you'r not authorized!")


@api_view(['GET'])
def company_list(request):
    result = Company.objects.all()
    serializer = CompanyListSerializer(result, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def createCompany(request):
    if request.user.is_authenticated:
        serializer = CompanySerializer(request.data)
        if serializer.is_valid():
            company = serializer.save()
            admin = CompanyAdmin.objects.create(company=company,user=request.user)
            admin.save()
            return Response('ok')
        return Response(serializer.error)
    return Response("not authorized")


def updateCompany(request):
    if request.user.is_authenticated:
        try:
            company = Company.objects.get(id=request.data['id'])
            admin = CompanyAdmin.objects.get(company=company)
        except:
            return Response('not found')
        if request.user == admin.user:
            serializer = CompanySerializer(instance=company, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response('ok')
            return Response(serializer.errors)
        return Response('not authorized')


@swagger_auto_schema(method='get', manual_parameters=[id_param])
@api_view(['GET'])
def get_company(request):
    req_serializer = GetCompanySerializer(data=request.data)
    if req_serializer.is_valid(raise_exception=True):
        req = req_serializer.data
    try:
        result = Company.objects.get(id=req["id"])
    except:
        return "does not exist"
    serializer = CompanySerializer(result, many=False)
    return Response(serializer.data)


@swagger_auto_schema(method='post', manual_parameters=[
    openapi.Parameter('company', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    openapi.Parameter('rating', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    openapi.Parameter('body', openapi.IN_QUERY, type=openapi.TYPE_STRING),
])
@api_view(['POST'])
def create_company_review(request):
    if request.user.is_authenticated:
        serializer = CompanyReviewSerializer(data=request.data)
        if serializer.is_valid():
            owner = Customer.objects.get(id=request.user.id)
            serializer.save(owner=owner)
            return Response('ok')
        return Response(serializer.errors)
    return Response('user not authenticated')

def update_company_review(request):
    if request.user.is_authenticated:
        try:
            review = Companyreview.objects.get(id=request.data['id'])

        except:
            return Response('not found')
        if request.user == review.owner.user:
            serializer = CompanyReviewSerializer(instance=review, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response('ok')
            return Response(serializer.errors)
        return Response('not authorized')


@swagger_auto_schema(method='get', manual_parameters=[id_param])
@api_view(['GET'])
def list_company_review(request):
    req_serializer = GetCompanySerializer(data=request.data)
    if req_serializer.is_valid(raise_exception=True):
        req = req_serializer.data
    try:
        company = Company.objects.get(id=req["id"])
    except:
        return "does not exist"
    reviews = company.companyreview_set.all()
    serializer = CompanyReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='post', manual_parameters=[
    openapi.Parameter('job', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    openapi.Parameter('linkdin', openapi.IN_QUERY, type=openapi.TYPE_STRING),
    openapi.Parameter('experience', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    openapi.Parameter('portfolio', openapi.IN_QUERY, type=openapi.TYPE_STRING),
    openapi.Parameter('description', openapi.IN_QUERY, type=openapi.TYPE_STRING),
],)
@api_view(['POST'])
def create_job_application(request):
    if request.user.is_authenticated:
        serializer = JobApplicationSerializer(data=request.data)
        if serializer.is_valid():
            customer = Customer.objects.get(user=request.user.id)
            serializer.save(customer=customer)
            return Response('ok')
        return Response(serializer.errors)
    return Response('user not authenticated')


@swagger_auto_schema(method='post', manual_parameters=[
    openapi.Parameter('company', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    openapi.Parameter('title_ar', openapi.IN_QUERY, type=openapi.TYPE_STRING),
    openapi.Parameter('title_en', openapi.IN_QUERY, type=openapi.TYPE_STRING),
    openapi.Parameter('title_fr', openapi.IN_QUERY, type=openapi.TYPE_STRING),
    openapi.Parameter('description', openapi.IN_QUERY, type=openapi.TYPE_STRING),
],)
@api_view(['POST'])
def create_job_offer(request):
    if request.user.is_authenticated:
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            admin = CompanyAdmin.objects.get(company=serializer.validated_data["company"])
            if request.user == admin.user:
                serializer.save()
                return Response('ok')
            return Response('you are not allowed')
        return Response(serializer.errors)
    return Response('not authorized')


@api_view(['GET'])
def list_job_offer(request):
    jobs = Job.objects.filter(open=True)
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='get', manual_parameters=[id_param])
@api_view(['GET'])
def get_job(request):
    request_serializer = GetJobSerializer(data=request.data)
    if request_serializer.is_valid():
        req = request_serializer.data
    try:
        job = Job.objects.get(id=req["id"])
    except:
        return Response("job doesn't exist")
    serializer = JobSerializer(job, many=False)
    return Response(serializer.data)


@swagger_auto_schema(method='put', manual_parameters=[id_param])
@api_view(['PUT'])
def close_job_offer(request):
    request_serializer = GetJobSerializer(data=request.data)
    if request_serializer.is_valid():
        req = request_serializer.data
        try:
            job = Job.objects.get(id=req["id"])
        except:
            return Response("job doesn't exist")
        job.open = False
        job.save()
    return Response("ok")


@swagger_auto_schema(method='get', manual_parameters=[id_param])
@api_view(['GET'])
def list_job_application(request):
    req = GetJobSerializer(request.data)
    try:
        job = Job.objects.get(id=req.data["id"])
    except:
        return Response("job doesn't exist")
    result = JobApplication.objects.filter(job=job)
    serializer = JobApplicationSerializer(result, many=True)
    return Response(serializer.data)














