"""
API views for the Research Groups app.

This file contains ViewSets and API views that handle HTTP requests and responses
for the research_groups API endpoints.
"""

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ResearchGroup
from .serializers import ResearchGroupSerializer, ResearchGroupListSerializer, MOOChubOrganizationSerializer

class ResearchGroupViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ResearchGroup model.
    
    This ViewSet automatically provides the following actions:
    'list', 'create', 'retrieve', 'update', 'partial_update', and 'destroy'.
    
    It handles all CRUD operations for ResearchGroup objects through the API.
    """
    
    queryset = ResearchGroup.objects.all()
    serializer_class = ResearchGroupSerializer
    
    # Add search and filtering capabilities
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']  # Fields that can be searched
    ordering_fields = ['name']  # Fields that can be used for ordering
    
    def get_serializer_class(self):
        """
        Return different serializers based on the action.
        
        For list views, use the simplified ResearchGroupListSerializer to improve performance.
        For all other actions, use the full ResearchGroupSerializer.
        """
        if self.action == 'list':
            return ResearchGroupListSerializer
        return ResearchGroupSerializer
    
    @action(detail=True, methods=['get'])
    def leader(self, request, pk=None):
        """
        Return the professor leading this research group.
        
        This is a custom endpoint that will be available at:
        /api/research_groups/{id}/leader/
        """
        group = self.get_object()
        if hasattr(group, 'lead_professor') and group.lead_professor:
            from professors.serializers import ProfessorSerializer  # Import here to avoid circular imports
            serializer = ProfessorSerializer(group.lead_professor)
            return Response(serializer.data)
        return Response({"detail": "No leader found for this research group."}, status=404)
    
    @action(detail=True, methods=['get'])
    def phd_students(self, request, pk=None):
        """
        Return all PhD students in this research group.
        
        This is a custom endpoint that will be available at:
        /api/research_groups/{id}/phd_students/
        """
        group = self.get_object()
        students = group.phd_students.all()
        from phd_students.serializers import PhDStudentSerializer  # Import here to avoid circular imports
        serializer = PhDStudentSerializer(students, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def courses(self, request, pk=None):
        """
        Return all courses associated with this research group.
        
        This is a custom endpoint that will be available at:
        /api/research_groups/{id}/courses/
        """
        group = self.get_object()
        courses = group.courses.all()
        from courses.serializers import CourseSerializer  # Import here to avoid circular imports
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

class MOOChubOrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for MOOChub-compatible Research Group API.
    
    This ViewSet provides read-only access to research groups in a format compatible with
    the MOOChub schema for interoperability with other platforms.
    
    Only 'list' and 'retrieve' actions are available since this is a read-only API.
    """
    
    queryset = ResearchGroup.objects.all()
    serializer_class = MOOChubOrganizationSerializer
    
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
        Override retrieve method to format single research group response according to MOOChub JSON:API spec.
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
