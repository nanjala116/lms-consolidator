"""
Serializers for the Courses app.

This file contains serializers that convert Course model instances into JSON representations
and vice versa, enabling API functionality for the courses app.
"""

from rest_framework import serializers
from courses.models import Course
from django.urls import reverse

class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model.
    
    This serializer handles the conversion between Course model instances and their
    JSON representation. It includes all fields from the Course model and adds
    additional computed fields for related data.
    """
    
    # Computed fields for related objects
    professor_names = serializers.SerializerMethodField()
    research_group_names = serializers.SerializerMethodField()
    
    class Meta:
        """
        Meta class to specify model and fields for the serializer.
        """
        model = Course
        fields = [
            'id', 'name', 'description', 'image_url', 'credits', 
            'code', 'start_date', 'end_date', 'format', 'level',
            'professor_names', 'research_group_names'
        ]
    
    def get_professor_names(self, obj):
        """Return a list of names of professors teaching this course."""
        return [str(professor) for professor in obj.professors.all()]
    
    def get_research_group_names(self, obj):
        """Return a list of research groups associated with this course."""
        return [str(group) for group in obj.research_groups.all()]

class CourseListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for Course list views.
    
    This serializer includes only the essential fields needed for list displays,
    optimizing performance by reducing data transfer.
    """
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'level', 'format', 'start_date']  # Only essential fields

# MOOChub compatible serializer
class MOOChubCourseSerializer(serializers.ModelSerializer):
    """
    Serializer specifically formatted for MOOChub API compatibility.
    
    This serializer maps our internal Course model fields to the field names and
    structure expected by the MOOChub schema for interoperability with other platforms.
    """
    
    # MOOChub specific field mappings
    type = serializers.SerializerMethodField()
    courseCode = serializers.CharField(source='code')
    courseMode = serializers.SerializerMethodField()
    inLanguage = serializers.SerializerMethodField()
    startDate = serializers.SerializerMethodField()
    endDate = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    instructor = serializers.SerializerMethodField()
    publisher = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'type', 'name', 'description', 'courseCode', 
            'courseMode', 'inLanguage', 'startDate', 'endDate',
            'duration', 'instructor', 'publisher', 'url', 'image',
            'credits', 'level'
        ]
    
    def get_type(self, obj):
        """Return the type of resource according to MOOChub schema."""
        return "Course"
    
    def get_courseMode(self, obj):
        """Convert our format to MOOChub courseMode."""
        # Map your format values to MOOChub's expected values
        if not obj.format:
            return ["online"]
            
        format_mapping = {
            'Self-paced': 'asynchronous',
            'Scheduled': 'synchronous',
            # Add other mappings as needed
        }
        return [format_mapping.get(obj.format.upper(), 'online')]
    
    def get_inLanguage(self, obj):
        """Return the language of the course in ISO format."""
        # Since our model doesn't have a language field, default to English
        return ["en"]
    
    def get_startDate(self, obj):
        """Return start date in ISO format as required by MOOChub."""
        if obj.start_date:
            return [obj.start_date.isoformat()]
        return []
    
    def get_endDate(self, obj):
        """Return end date in ISO format as required by MOOChub."""
        if obj.end_date:
            return [obj.end_date.isoformat()]
        return []
    
    def get_duration(self, obj):
        """
        Convert course credits or level to ISO 8601 duration format (hours) for MOOChub.

        - For MBA, Master, and Micro Degree: 1 credit = 25 hours.
        - For Basic (open courses): always 14 hours.
        - If level is missing or unrecognized, default to Basic (14 hours).
        """
        hours = None
        level = getattr(obj, 'level', None)
        if level:
            # Ensure case-insensitive comparison, but match database capitalization
            if level in ['MBA', 'Master', 'Micro Degree']:
                # For MBA, Master, and Micro Degree, 1 credit = 25 hours
                hours = obj.credits * 25 if obj.credits else None
            elif level == 'Basics':
                hours = 14
            else:
                hours = obj.credits * 25 if obj.credits else 14
        else:
            # Default to Basic if level is missing
            hours = 14

        return f"PT{hours}H" if hours else None
    
    def get_instructor(self, obj):
        """Return instructors in MOOChub format."""
        instructors = []
        for professor in obj.professors.all():
            instructors.append({
                "type": "Person",
                "name": str(professor),
                "honorificPrefix": professor.title if hasattr(professor, 'title') else "",
            })
        return instructors
    
    def get_publisher(self, obj):
        """Return publisher information for MOOChub."""
        return {
            "type": "Organization",
            "name": "German University of Digital Science"
        }
    
    def get_url(self, obj):
        """Return the absolute URL for this course using Django's reverse()."""
        request = self.context.get('request')
        url = reverse('courses:course-detail', kwargs={'pk': obj.pk})
        if request is not None:
            return request.build_absolute_uri(url)
        return url
    
    def get_image(self, obj):
        """Return image information in MOOChub format."""
        if obj.image_url:
            return {
                "type": "ImageObject",
                "contentUrl": obj.image_url,
            }
        return None
