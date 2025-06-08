"""
API views for the PhD Students app.

This file contains ViewSets and API views that handle HTTP requests and responses
for the phd_students API endpoints.
"""

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import PhDStudent
from .serializers import PhDStudentSerializer, PhDStudentListSerializer, MOOChubPhDStudentSerializer

class PhDStudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for PhDStudent model.
    
    This ViewSet automatically provides the following actions:
    'list', 'create', 'retrieve', 'update', 'partial_update', and 'destroy'.
    
    It handles all CRUD operations for PhDStudent objects through the API.
    """
    
    queryset = PhDStudent.objects.all()
    serializer_class = PhDStudentSerializer
    
    # Add search and filtering capabilities
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'title']  # Fields that can be searched
    ordering_fields = ['name', 'enrollment_date']  # Fields that can be used for ordering
    
    def get_serializer_class(self):
        """
        Return different serializers based on the action.
        
        For list views, use the simplified PhDStudentListSerializer to improve performance.
        For all other actions, use the full PhDStudentSerializer.
        """
        if self.action == 'list':
            return PhDStudentListSerializer
        return PhDStudentSerializer
    
    @action(detail=True, methods=['get'])
    def supervisor(self, request, pk=None):
        """
        Return the supervisor of this PhD student.
        
        This is a custom endpoint that will be available at:
        /api/phd_students/{id}/supervisor/
        """
        student = self.get_object()
        supervisor = student.supervisor
        if supervisor:
            from professors.serializers import ProfessorSerializer  # Import here to avoid circular imports
            serializer = ProfessorSerializer(supervisor)
            return Response(serializer.data)
        return Response({"detail": "No supervisor found for this student."}, status=404)
    
    @action(detail=True, methods=['get'])
    def research_group(self, request, pk=None):
        """
        Return the research group this PhD student belongs to.
        
        This is a custom endpoint that will be available at:
        /api/phd_students/{id}/research_group/
        """
        student = self.get_object()
        group = student.research_group
        if group:
            from research_groups.serializers import ResearchGroupSerializer  # Import here to avoid circular imports
            serializer = ResearchGroupSerializer(group)
            return Response(serializer.data)
        return Response({"detail": "No research group found for this student."}, status=404)
    
    def get_queryset(self):
        """
        Optionally filter the PhD students by supervisor or research group.
        
        This allows API endpoints like:
        /api/phd_students/?supervisor_id=1
        /api/phd_students/?research_group_id=2
        """
        queryset = PhDStudent.objects.all()
        
        # Filter by supervisor if provided in query params
        supervisor_id = self.request.query_params.get('supervisor_id', None)
        if supervisor_id is not None:
            queryset = queryset.filter(supervisor_id=supervisor_id)
        
        # Filter by research group if provided in query params
        research_group_id = self.request.query_params.get('research_group_id', None)
        if research_group_id is not None:
            queryset = queryset.filter(research_group_id=research_group_id)
        
        return queryset

class MOOChubPhDStudentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for MOOChub-compatible PhD Student API.
    
    This ViewSet provides read-only access to PhD students in a format compatible with
    the MOOChub schema for interoperability with other platforms.
    
    Only 'list' and 'retrieve' actions are available since this is a read-only API.
    """
    
    queryset = PhDStudent.objects.all()
    serializer_class = MOOChubPhDStudentSerializer
    
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
        Override retrieve method to format single PhD student response according to MOOChub JSON:API spec.
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
