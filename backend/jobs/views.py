from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import JobPosting
from .serializers import JobPostingSerializer
from .permissions import IsEmployer, IsOwner


class JobListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsEmployer()]

        return [AllowAny()]

    def get(self, request):
        jobs = JobPosting.objects.filter(is_active=True)
        serializer = JobPostingSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JobPostingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(employer=request.user)

        return Response(
            {"message": "Job created successfully"},
            status=status.HTTP_201_CREATED,
        )


class JobDetailView(APIView):
    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE"]:
            return [IsOwner()]
        return [AllowAny()]

    def get(self, request, id):
        job = get_object_or_404(JobPosting, id=id)
        serializer = JobPostingSerializer(job)
        return Response(serializer.data)

    def patch(self, request, id):
        job = get_object_or_404(JobPosting, id=id)
        self.check_object_permissions(request, job)
        serializer = JobPostingSerializer(job, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Job updated successfully"},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, id):
        job = get_object_or_404(JobPosting, id=id)
        self.check_object_permissions(request, job)
        job.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
