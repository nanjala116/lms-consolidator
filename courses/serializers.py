"""
Serializers for the Courses app.

This file contains serializers that convert Course model instances into JSON representations
and vice versa, enabling API functionality for the courses app.
"""

from rest_framework import serializers
from courses.models import Course

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
            'SELF_PACED': 'asynchronous',
            'SCHEDULED': 'synchronous',
            'BLENDED': 'blended',
            'ONLINE': 'online',
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
        """Convert credits to ISO 8601 duration format (hours)."""
        if obj.credits:
            # For master's: 5 credits = 125 hours, so 1 credit = 25 hours
            # For MBA: 4 credits = 120 hours, so 1 credit = 30 hours
            # For Master's: 5 credits = 125 hours, so 1 credit = 25 hours
            # For Standalone: assume 1 credit = 20 hours
            if hasattr(obj, 'level') and obj.level:
                level = obj.level.upper()
                if level == 'MBA':
                    hours = obj.credits * 30
                elif level == 'MASTERS':
                    hours = obj.credits * 25
                elif level == 'STANDALONE':
                    hours = obj.credits * 20
                else:
                    hours = obj.credits * 25  # Default to master's
            else:
                hours = obj.credits * 25  # Default to master's
            return f"PT{hours}H"
        return None
    
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
        """Return the URL for this course."""
        # Use a generic URL pattern with the course code
        return f"https://german-uds.academy/courses/{obj.code}"
    
    def get_image(self, obj):
        """Return image information in MOOChub format."""
        if obj.image_url:
            return {
                "type": "ImageObject",
                "contentUrl": obj.image_url,
            }
        return None
