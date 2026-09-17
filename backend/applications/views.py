from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsSeeker
from jobs.permissions import IsEmployer
from .serializers import ApplicationSerializer, ApplicationStatusSerializer
from .models import Application
from jobs.models import JobPosting


class ApplyJobView(APIView):
    def get_permissions(self):
        return [IsSeeker()]

    def post(self, request, id):
        job = get_object_or_404(JobPosting, id=id)
        serializer = ApplicationSerializer(data=request.data)
        if not job.is_active:
            return Response(
                {"message": "This job is no longer active"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.is_valid(raise_exception=True)
        already_applied = Application.objects.filter(
            job=job, applicant=request.user
        ).exists()

        if already_applied:
            return Response(
                {"message": "You have already applied for this job."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save(applicant=request.user, job=job)
        return Response(
            {"message": "Application submitted successfully"},
            status=status.HTTP_201_CREATED,
        )


class JobApplicantView(APIView):
    def get_permissions(self):
        return [IsEmployer()]

    def get(self, request, id):
        job = get_object_or_404(JobPosting, id=id)
        if job.employer != request.user:
            return Response(
                {"message": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        applicants = Application.objects.filter(job=job)
        serializer = ApplicationSerializer(applicants, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class SeekerApplicationsView(APIView):
    def get_permissions(self):
        return [IsSeeker()]

    def get(self, request):
        applications = Application.objects.filter(applicant=request.user)
        serializer = ApplicationSerializer(applications, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class UpdateApplicationStatusView(APIView):
    def get_permissions(self):
        return [IsEmployer()]

    def patch(self, request, id):
        application = get_object_or_404(Application, id=id)
        serializer = ApplicationStatusSerializer(
            application, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        if application.job.employer != request.user:
            return Response(
                {"message": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer.save()
        return Response(
            {"message": "Application status updated successfully"},
            status=status.HTTP_200_OK,
        )
