from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from common.permissions import IsEmployer
from django.shortcuts import get_object_or_404
from .models import CompanyProfile
from .serializers import CompanyProfileSerializer


class CompanyProfileView(APIView):
    def get_permissions(self):
        return [IsEmployer()]

    def get(self, request):
        company = get_object_or_404(CompanyProfile, user=request.user)
        serializer = CompanyProfileSerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if CompanyProfile.objects.filter(user=request.user).exists():
            return Response(
                {"error": "Company profile already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = CompanyProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(
            {"message": "Company profile created"}, status=status.HTTP_201_CREATED
        )

    def patch(self, request):
        company = get_object_or_404(CompanyProfile, user=request.user)
        serializer = CompanyProfileSerializer(company, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Company profile updated"}, status=status.HTTP_200_OK
        )


class CompanyDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        company = get_object_or_404(CompanyProfile, id=id)
        serializer = CompanyProfileSerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)
