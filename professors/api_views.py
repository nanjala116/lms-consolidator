"""
API views for the Professors app.

This file contains ViewSets and API views that handle HTTP requests and responses
for the professors API endpoints.
"""

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Professor
from .serializers import ProfessorSerializer, ProfessorListSerializer, MOOChubPersonSerializer

class ProfessorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Professor model.
    
    This ViewSet automatically provides the following actions:
    'list', 'create', 'retrieve', 'update', 'partial_update', and 'destroy'.
    
    It handles all CRUD operations for Professor objects through the API.
    """
    
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    
    # Add search capabilities
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'position']  # Fields that can be searched
    ordering_fields = ['name', 'title']  # Fields that can be used for ordering
    
    def get_serializer_class(self):
        """
        Return different serializers based on the action.
        
        For list views, use the simplified ProfessorListSerializer to improve performance.
        For all other actions, use the full ProfessorSerializer.
        """
        if self.action == 'list':
            return ProfessorListSerializer
        return ProfessorSerializer
    
    @action(detail=True, methods=['get'])
    def courses(self, request, pk=None):
        """
        Return all courses taught by this professor.
        
        This is a custom endpoint that will be available at:
        /api/professors/{id}/courses/
        """
        professor = self.get_object()
        courses = professor.courses.all()
        from courses.serializers import CourseSerializer  # Import here to avoid circular imports
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def phd_students(self, request, pk=None):
        """
        Return all PhD students supervised by this professor.
        
        This is a custom endpoint that will be available at:
        /api/professors/{id}/phd_students/
        """
        professor = self.get_object()
        students = professor.phd_students.all()
        from phd_students.serializers import PhDStudentSerializer  # Import here to avoid circular imports
        serializer = PhDStudentSerializer(students, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def research_group(self, request, pk=None):
        """
        Return the research group led by this professor.
        
        This is a custom endpoint that will be available at:
        /api/professors/{id}/research_group/
        """
        professor = self.get_object()
        if hasattr(professor, 'leads_research_group') and professor.leads_research_group:
            from research_groups.serializers import ResearchGroupSerializer  # Import here to avoid circular imports
            serializer = ResearchGroupSerializer(professor.leads_research_group)
            return Response(serializer.data)
        return Response({"detail": "No research group found for this professor."}, status=404)

class MOOChubPersonViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for MOOChub-compatible Professor API.
    
    This ViewSet provides read-only access to professors in a format compatible with
    the MOOChub schema for interoperability with other platforms.
    
    Only 'list' and 'retrieve' actions are available since this is a read-only API.
    """
    
    queryset = Professor.objects.all()
    serializer_class = MOOChubPersonSerializer
    
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
        Override retrieve method to format single professor response according to MOOChub JSON:API spec.
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
