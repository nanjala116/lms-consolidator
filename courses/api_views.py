"""
API views for the Courses app.

This file contains ViewSets and API views that handle HTTP requests and responses
for the courses API endpoints.
"""

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Course
from .serializers import CourseSerializer, CourseListSerializer, MOOChubCourseSerializer

class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Course model.
    
    This ViewSet automatically provides the following actions:
    'list', 'create', 'retrieve', 'update', 'partial_update', and 'destroy'.
    
    It handles all CRUD operations for Course objects through the API.
    """
    
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    # Add search and filtering capabilities
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code', 'description']  # Fields that can be searched
    ordering_fields = ['name', 'start_date', 'level']  # Fields that can be used for ordering
    
    def get_serializer_class(self):
        """
        Return different serializers based on the action.
        
        For list views, use the simplified CourseListSerializer to improve performance.
        For all other actions, use the full CourseSerializer.
        """
        if self.action == 'list':
            return CourseListSerializer
        return CourseSerializer
    
    @action(detail=True, methods=['get'])
    def professors(self, request, pk=None):
        """
        Return all professors teaching this course.
        
        This is a custom endpoint that will be available at:
        /api/courses/{id}/professors/
        """
        course = self.get_object()
        professors = course.professors.all()
        from professors.serializers import ProfessorSerializer  # Import here to avoid circular imports
        serializer = ProfessorSerializer(professors, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def research_groups(self, request, pk=None):
        """
        Return all research groups associated with this course.
        
        This is a custom endpoint that will be available at:
        /api/courses/{id}/research_groups/
        """
        course = self.get_object()
        groups = course.research_groups.all()
        from research_groups.serializers import ResearchGroupSerializer  # Import here to avoid circular imports
        serializer = ResearchGroupSerializer(groups, many=True)
        return Response(serializer.data)

class MOOChubCourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for MOOChub-compatible Course API.
    
    This ViewSet provides read-only access to courses in a format compatible with
    the MOOChub schema for interoperability with other platforms.
    
    Only 'list' and 'retrieve' actions are available since this is a read-only API.
    """
    
    queryset = Course.objects.all()
    serializer_class = MOOChubCourseSerializer
    
    def list(self, request, *args, **kwargs):
        """
        Override list method to format response according to MOOChub JSON:API spec.
        
        This ensures the response structure follows the MOOChub requirements,
        including proper pagination links and metadata.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data)
            
            # Format according to MOOChub JSON:API spec
            formatted_data = {
                "jsonapi": {"version": "1.0"},
                "data": data.data['results'],
                "links": {
                    "self": request.build_absolute_uri(),
                }
            }
            
            # Add pagination links if available
            if 'links' in data.data:
                if data.data['links'].get('next'):
                    formatted_data['links']['next'] = data.data['links']['next']
                
                if data.data['links'].get('previous'):
                    formatted_data['links']['prev'] = data.data['links']['previous']
                    
            return Response(formatted_data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({"jsonapi": {"version": "1.0"}, "data": serializer.data})
    
    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve method to format single course response according to MOOChub JSON:API spec.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # Format according to MOOChub JSON:API spec
        formatted_data = {
            "jsonapi": {"version": "1.0"},
            "data": serializer.data,
            "links": {
                "self": request.build_absolute_uri()
            }
        }
        
        return Response(formatted_data)
