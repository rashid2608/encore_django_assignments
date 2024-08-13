from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import requests
import logging

logger = logging.getLogger(__name__)

class CourseListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info("Received GET request for courses")
        page = request.query_params.get('page', '1')
        page_size = request.query_params.get('page_size', '5')
        fields = request.query_params.get('fields', '')

        edx_api_url = f"https://courses.edx.org/api/courses/v1/courses/?page={page}&page_size={page_size}"
        response = requests.get(edx_api_url)
        
        if response.status_code == 200:
            data = response.json()
            
            if fields:
                field_list = fields.split(',')
                filtered_results = []
                for course in data['results']:
                    filtered_course = {field: course.get(field) for field in field_list if field in course}
                    filtered_results.append(filtered_course)
                data['results'] = filtered_results

            logger.info("Successfully retrieved and processed courses")
            return Response(data)
        else:
            logger.error(f"Failed to fetch courses from edX API. Status code: {response.status_code}")
            return Response({"error": "Failed to fetch courses from edX API"}, status=response.status_code)
