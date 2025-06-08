"""
Serializers for the Research Groups app.

This file contains serializers that convert ResearchGroup model instances into JSON representations
and vice versa, enabling API functionality for the research_groups app.
"""

from rest_framework import serializers
from research_groups.models import ResearchGroup

class ResearchGroupSerializer(serializers.ModelSerializer):
    """
    Serializer for the ResearchGroup model.
    
    This serializer handles the conversion between ResearchGroup model instances and their
    JSON representation. It includes all fields from the ResearchGroup model and adds
    additional computed fields for related data.
    """
    
    # Computed fields for related objects
    lead_professor_name = serializers.SerializerMethodField()
    phd_student_count = serializers.SerializerMethodField()
    
    class Meta:
        """
        Meta class to specify model and fields for the serializer.
        """
        model = ResearchGroup
        fields = [
            'id', 'name', 'description', 
            'lead_professor_name', 'phd_student_count'
        ]
    
    def get_lead_professor_name(self, obj):
        """Return the name of the professor leading this research group."""
        if hasattr(obj, 'lead_professor') and obj.lead_professor:
            return obj.lead_professor.name
        return None
    
    def get_phd_student_count(self, obj):
        """Return the number of PhD students in this research group."""
        return obj.phd_students.count()

class ResearchGroupListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for ResearchGroup list views.
    
    This serializer includes only the essential fields needed for list displays,
    optimizing performance by reducing data transfer.
    """
    
    # Include leader name directly in the list view
    lead_professor_name = serializers.SerializerMethodField()
    
    class Meta:
        model = ResearchGroup
        fields = ['id', 'name', 'lead_professor_name']  # Only essential fields
    
    def get_lead_professor_name(self, obj):
        """Return the name of the professor leading this research group."""
        if hasattr(obj, 'lead_professor') and obj.lead_professor:
            return obj.lead_professor.name
        return None

# MOOChub compatible serializer for Research Groups
class MOOChubOrganizationSerializer(serializers.ModelSerializer):
    """
    Serializer specifically formatted for MOOChub API compatibility.
    
    This serializer maps our internal ResearchGroup model fields to the field names and
    structure expected by the MOOChub schema for interoperability with other platforms.
    """
    
    # MOOChub specific field mappings
    type = serializers.SerializerMethodField()
    identifier = serializers.SerializerMethodField()
    member = serializers.SerializerMethodField()
    
    class Meta:
        model = ResearchGroup
        fields = [
            'id', 'type', 'name', 'description', 
            'identifier', 'member'
        ]
    
    def get_type(self, obj):
        """Return the type of resource according to MOOChub schema."""
        return "Organization"
    
    def get_identifier(self, obj):
        """Return a unique identifier for this research group."""
        return f"research-group-{obj.id}"
    
    def get_member(self, obj):
        """Return members of this research group in MOOChub format."""
        members = []
        
        # Add lead professor if available
        if hasattr(obj, 'lead_professor') and obj.lead_professor:
            members.append({
                "type": "Person",
                "name": obj.lead_professor.name,
                "honorificPrefix": obj.lead_professor.title if hasattr(obj.lead_professor, 'title') else "",
                "roleName": "Lead"
            })
        
        # Add PhD students
        for student in obj.phd_students.all():
            members.append({
                "type": "Person",
                "name": student.name,
                "honorificPrefix": student.title if student.title else "",
                "roleName": "PhD Student"
            })
            
        return members
