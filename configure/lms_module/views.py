from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import permissions
from user_profile.function_call import *
from django.db import IntegrityError            
import random
from django.db.models import Q


class DepartmentAddView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetDepartmentSerializer
    queryset = Department.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]  # Add the filter backend for search functionality
    ordering_fields = ['department_name']
    search_fields = ['department_name']

    def create(self,request):
            try:
                department_name = request.data.get('department_name')
                department_description = request.data.get('department_description')

                if not department_name:
                    return Response({'status': False,'message': 'Department name is required'})
                if not department_description:
                    return Response({'status': False,'message': 'Department description is required'})
                    

                department_obj = Department.objects.create(department_name=department_name,department_description=department_description)
                department_obj.save()
                return Response({'status': True,'message':"Department created successfully"})
            except Exception as e:
                return Response({"status": False,'message': 'Something went wrong','error': str(e)})
      
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        try:
            if queryset.exists():
                serializer_data = []
                for obj in queryset:
                    context = {'request': request}  # Removed the serial number from the context
                    serializer = GetDepartmentSerializer(obj, context=context)
                    serializer_data.append(serializer.data)

                count = len(serializer_data)
                return Response({
                    "status": True,
                    "message": "Department data fetched successfully",
                    'total_page': 1,  # Since there is no pagination, the total pages will always be 1
                    'total': count,
                    'data': serializer_data
                })
            else:
                return Response({
                    "status": True,
                    "message": "No Department found",
                    "total_page": 0,
                    "total": 0,
                    "data": []
                })
        except Exception as e:
            return Response({"status": False, 'message': 'Something went wrong', 'error': str(e)})


               
class DepartmentUpdatesViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'department_id'

    def update(self, request, *args, **kwargs):
    
        try:
            department_id = self.kwargs.get("department_id")
            department_name = request.data.get('department_name')
            department_description = request.data.get('department_description')
    
            if not Department.objects.filter(id=department_id).exists():
                return Response({"status": False, "message": "Department id not found"})
    
            department_object = Department.objects.get(id=department_id)
            if department_name:
                department_object.department_name = department_name
            if department_description:
                department_object.department_description = department_description
            department_object.save()
    
            return Response({"status": True, "message": "Department updated successfully"})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})    
            
    def destroy(self, request, *args, **kwargs):
        if not request.user.has_perm('dashboard_app.delete_departmentmaster'):
                return Response({"status": False, "message": "You are not authorized to delete department!", "data": []})
        try:
            department_id = request.data.get('department_id')   
            if not Department.objects.filter(id=department_id):
                return Response({"status":False, "message":"Department id not found"})
                     
            department_object = Department.objects.get(id=department_id)
            department_object.delete()
            return Response({"status":True, "message":"Department deleted succesfully"})
        except Exception as e:
                return Response({"status": False,'message': 'Something went wrong','error': str(e)})
            

class PlantAddView(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetPlantSerializer
    queryset = Plant.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['plant_name']
    search_fields = ['plant_name']

    def create(self, request):
        try:
            plant_name = request.data.get('plant_name')
            plant_location = request.data.get('plant_location')
            plant_description = request.data.get('plant_description')

            if not plant_name:
                return Response({'status': False, 'message': 'Plant name is required'})
            if not plant_location:
                return Response({'status': False, 'message': 'Plant location is required'})
            if not plant_description:
                return Response({'status': False, 'message': 'Plant description is required'})

            plant_obj = Plant.objects.create(plant_name=plant_name, plant_location=plant_location, plant_description=plant_description)
            plant_obj.save()
            return Response({'status': True, 'message': "Plant created successfully"})
        except Exception as e:
            return Response({"status": False, 'message': 'Something went wrong', 'error': str(e)})

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        try:
            if queryset.exists():
                serializer_data = []
                for obj in queryset:
                    context = {'request': request}  # No serial number needed
                    serializer = GetPlantSerializer(obj, context=context)
                    serializer_data.append(serializer.data)

                count = len(serializer_data)
                return Response({
                    "status": True,
                    "message": "Plant data fetched successfully",
                    'total_page': 1, 
                    'total': count,
                    'data': serializer_data
                })
            else:
                return Response({
                    "status": True,
                    "message": "No Plant found",
                    "total_page": 0,
                    "total": 0,
                    "data": []
                })
        except Exception as e:
            return Response({"status": False, 'message': 'Something went wrong', 'error': str(e)})


class PlantUpdatesViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'plant_id'

    def update(self, request, *args, **kwargs):
        if not request.user.has_perm('dashboard_app.change_plant'):
            return Response({"status": False, "message": "You are not authorized to update plant!", "data": []})

        try:
            plant_id = self.kwargs.get("plant_id")
            plant_name = request.data.get('plant_name')
            plant_location = request.data.get('plant_location')
            plant_description = request.data.get('plant_description')

            # Check if the plant exists
            if not Plant.objects.filter(id=plant_id).exists():
                return Response({"status": False, "message": "Plant ID not found"})

            # Fetch the plant object
            plant_object = Plant.objects.get(id=plant_id)

            # Update plant details if provided
            if plant_name:
                plant_object.plant_name = plant_name
            if plant_location:
                plant_object.plant_location = plant_location
            if plant_description:
                plant_object.plant_description = plant_description
            plant_object.save()

            return Response({"status": True, "message": "Plant updated successfully"})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})

    def destroy(self, request, *args, **kwargs):
        if not request.user.has_perm('dashboard_app.delete_plant'):
            return Response({"status": False, "message": "You are not authorized to delete plant!", "data": []})

        try:
            plant_id = request.data.get('plant_id')

            # Check if the plant exists
            if not Plant.objects.filter(id=plant_id).exists():
                return Response({"status": False, "message": "Plant ID not found"})

            # Delete the plant
            plant_object = Plant.objects.get(id=plant_id)
            plant_object.delete()

            return Response({"status": True, "message": "Plant deleted successfully"})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})


class JobRoleAddView(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]  # Uncomment if authentication is required
    serializer_class = GetJobRoleSerializer
    queryset = JobRole.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]  # Add search and ordering filters
    ordering_fields = ['job_role_name']  # Fields you want to enable ordering on
    search_fields = ['job_role_name']  # Fields you want to enable search on

    def create(self, request):
        try:
            job_role_name = request.data.get('job_role_name')
            job_role_description = request.data.get('job_role_description')

            if not job_role_name:
                return Response({'status': False, 'message': 'Job role name is required'})
            if not job_role_description:
                return Response({'status': False, 'message': 'Job role description is required'})

            job_role_obj = JobRole.objects.create(
                job_role_name=job_role_name,
                job_role_description=job_role_description
            )
            job_role_obj.save()

            return Response({'status': True, 'message': "Job role created successfully"})
        except Exception as e:
            return Response({"status": False, 'message': 'Something went wrong', 'error': str(e)})

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        try:
            if queryset.exists():
                serializer_data = []
                for obj in queryset:
                    context = {'request': request}  # No serial number needed
                    serializer = GetJobRoleSerializer(obj, context=context)
                    serializer_data.append(serializer.data)

                count = len(serializer_data)
                return Response({
                    "status": True,
                    "message": "Job role data fetched successfully",
                    'total_page': 1,  # Total pages can always be 1 without pagination
                    'total': count,
                    'data': serializer_data
                })
            else:
                return Response({
                    "status": True,
                    "message": "No Job role found",
                    "total_page": 0,
                    "total": 0,
                    "data": []
                })
        except Exception as e:
            return Response({"status": False, 'message': 'Something went wrong', 'error': str(e)})


class JobRoleUpdatesViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'job_role_id'

    def update(self, request, *args, **kwargs):
        if not request.user.has_perm('dashboard_app.change_jobrole'):
            return Response({"status": False, "message": "You are not authorized to update job role!", "data": []})

        try:
            job_role_id = self.kwargs.get("job_role_id")
            job_role_name = request.data.get('job_role_name')
            job_role_description = request.data.get('job_role_description')

            # Check if the job role exists
            if not JobRole.objects.filter(id=job_role_id).exists():
                return Response({"status": False, "message": "Job role ID not found"})

            # Fetch the job role object
            job_role_object = JobRole.objects.get(id=job_role_id)

            # Update job role details if provided
            if job_role_name:
                job_role_object.job_role_name = job_role_name
            if job_role_description:
                job_role_object.job_role_description = job_role_description
            job_role_object.save()

            return Response({"status": True, "message": "Job role updated successfully"})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})

    def destroy(self, request, *args, **kwargs):
        if not request.user.has_perm('dashboard_app.delete_jobrole'):
            return Response({"status": False, "message": "You are not authorized to delete job role!", "data": []})

        try:
            job_role_id = request.data.get('job_role_id')

            # Check if the job role exists
            if not JobRole.objects.filter(id=job_role_id).exists():
                return Response({"status": False, "message": "Job role ID not found"})

            # Delete the job role
            job_role_object = JobRole.objects.get(id=job_role_id)
            job_role_object.delete()

            return Response({"status": True, "message": "Job role deleted successfully"})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})


class AreaAddView(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]  # Uncomment if authentication is required
    serializer_class = GetAreaSerializer
    queryset = Area.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]  # Add search and ordering filters
    ordering_fields = ['area_name']  # Fields you want to enable ordering on
    search_fields = ['area_name', 'department__department_name']  # Fields you want to enable search on, including related department name

    def create(self, request):
        try:
            area_name = request.data.get('area_name')
            department_id = request.data.get('department_id')
            area_description = request.data.get('area_description')

            # Validate required fields
            if not area_name:
                return Response({'status': False, 'message': 'Area name is required'})
            if not department_id:
                return Response({'status': False, 'message': 'Department ID is required'})
            if not area_description:
                return Response({'status': False, 'message': 'Area description is required'})

            # Validate if the department exists
            if not Department.objects.filter(id=department_id).exists():
                return Response({'status': False, 'message': 'Department ID not found'})

            # Create Area object
            area_obj = Area.objects.create(
                area_name=area_name,
                department_id=department_id,
                area_description=area_description
            )
            area_obj.save()

            return Response({'status': True, 'message': "Area created successfully"})
        except Exception as e:
            return Response({"status": False, 'message': 'Something went wrong', 'error': str(e)})

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        try:
            if queryset.exists():
                serializer_data = []
                for obj in queryset:
                    context = {'request': request}  # No serial number needed
                    serializer = GetAreaSerializer(obj, context=context)
                    serializer_data.append(serializer.data)

                count = len(serializer_data)
                return Response({
                    "status": True,
                    "message": "Area data fetched successfully",
                    'total_page': 1,  # Total pages can always be 1 without pagination
                    'total': count,
                    'data': serializer_data
                })
            else:
                return Response({
                    "status": True,
                    "message": "No Area found",
                    "total_page": 0,
                    "total": 0,
                    "data": []
                })
        except Exception as e:
            return Response({"status": False, 'message': 'Something went wrong', 'error': str(e)})


class AreaUpdatesViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'area_id'

    def update(self, request, *args, **kwargs):
        if not request.user.has_perm('dashboard_app.change_area'):
            return Response({"status": False, "message": "You are not authorized to update area!", "data": []})

        try:
            area_id = self.kwargs.get("area_id")
            area_name = request.data.get('area_name')
            department_id = request.data.get('department_id')
            area_description = request.data.get('area_description')

            # Check if the area exists
            if not Area.objects.filter(id=area_id).exists():
                return Response({"status": False, "message": "Area ID not found"})

            # Fetch the area object
            area_object = Area.objects.get(id=area_id)

            # Update area details if provided
            if area_name:
                area_object.area_name = area_name
            if department_id:
                if not Department.objects.filter(id=department_id).exists():
                    return Response({"status": False, "message": "Department ID not found"})
                area_object.department_id = department_id
            if area_description:
                area_object.area_description = area_description
            area_object.save()

            return Response({"status": True, "message": "Area updated successfully"})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})

    def destroy(self, request, *args, **kwargs):
        if not request.user.has_perm('dashboard_app.delete_area'):
            return Response({"status": False, "message": "You are not authorized to delete area!", "data": []})

        try:
            area_id = request.data.get('area_id')

            if not Area.objects.filter(id=area_id).exists():
                return Response({"status": False, "message": "Area ID not found"})

            area_object = Area.objects.get(id=area_id)
            area_object.delete()

            return Response({"status": True, "message": "Area deleted successfully"})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})


class AssessmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentSerializer
    queryset = Assessment.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['title']
    search_fields = ['title', 'sop_selection', 'assign']  # You can add more fields for searching if needed

    def create(self, request):
        try:
            title = request.data.get('title')
            time_limit = request.data.get('time_limit')
            sop_selection = request.data.get('sop_selection')
            assign = request.data.get('assign')
            pass_percentage = request.data.get('pass_percentage')
            number_of_attempts = request.data.get('number_of_attempts')

            # Validation
            if not title:
                return Response({'status': False, 'message': 'Title is required'})
            if not time_limit:
                return Response({'status': False, 'message': 'Time limit is required'})
            if not sop_selection:
                return Response({'status': False, 'message': 'SOP selection is required'})
            if not assign:
                return Response({'status': False, 'message': 'Assignment (Department/User) is required'})
            if not pass_percentage:
                return Response({'status': False, 'message': 'Pass percentage is required'})
            if not number_of_attempts:
                return Response({'status': False, 'message': 'Number of attempts is required'})

            # Create Assessment
            assessment_obj = Assessment.objects.create(
                title=title,
                time_limit=time_limit,
                sop_selection=sop_selection,
                assign=assign,
                pass_percentage=pass_percentage,
                number_of_attempts=number_of_attempts,
                created_at=timezone.now()
            )
            assessment_obj.save()

            return Response({'status': True, 'message': 'Assessment created successfully'})
        except Exception as e:
            return Response({"status": False, 'message': 'Something went wrong', 'error': str(e)})

    def list(self, request):
        queryset = Assessment.objects.all().order_by('-id')  # Fetching all assessments and ordering them by '-id'
        
        try:
            if queryset.exists():
                serializer = AssessmentSerializer(queryset, many=True)  # Serializing the queryset
                return Response({
                    "status": True,
                    "message": "Assessments fetched successfully",
                    'total': queryset.count(),  # Total number of assessments
                    'data': serializer.data
                })
            else:
                return Response({
                    "status": True,
                    "message": "No Assessments found",
                    "total": 0,
                    "data": []
                })
        except Exception as e:
            return Response({"status": False, 'message': 'Something went wrong', 'error': str(e)})

class AssessmentUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'assessment_id'  # Use this to specify the field used for lookup (e.g., 'assessment_id')

    def update(self, request, *args, **kwargs):
        # Check if the user has the permission to change assessments
        if not request.user.has_perm('app_name.change_assessment'):  # Replace 'app_name' with your app's name
            return Response({"status": False, "message": "You are not authorized to update assessment!", "data": []})

        try:
            # Get the assessment ID from the URL
            assessment_id = self.kwargs.get("assessment_id")
            
            # Get data from the request
            title = request.data.get('title')
            time_limit = request.data.get('time_limit')
            sop_selection = request.data.get('sop_selection')
            assign = request.data.get('assign')
            pass_percentage = request.data.get('pass_percentage')
            number_of_attempts = request.data.get('number_of_attempts')

            # Check if the assessment exists
            if not Assessment.objects.filter(id=assessment_id).exists():
                return Response({"status": False, "message": "Assessment ID not found"})

            # Fetch the assessment object
            assessment_object = Assessment.objects.get(id=assessment_id)

            # Update the assessment details if provided
            if title:
                assessment_object.title = title
            if time_limit:
                assessment_object.time_limit = time_limit
            if sop_selection:
                assessment_object.sop_selection = sop_selection
            if assign:
                assessment_object.assign = assign
            if pass_percentage:
                assessment_object.pass_percentage = pass_percentage
            if number_of_attempts:
                assessment_object.number_of_attempts = number_of_attempts
            
            # Save the updated assessment object
            assessment_object.save()

            return Response({"status": True, "message": "Assessment updated successfully"})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})

class AssessmentQuestionViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentQuestionSerializer
    queryset = AssessmentQuestion.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['created_at']
    search_fields = ['sop', 'created_by__full_name', 'department__name']

    def create(self, request):
        try:
            department = request.data.get('department')
            sop = request.data.get('sop')
            questions_data = request.data.get('questions_data')
            marks = request.data.get('marks')
            created_by = request.user  # Assuming user is authenticated

            # Validation
            if not department:
                return Response({'status': False, 'message': 'Department is required'})
            if not questions_data:
                return Response({'status': False, 'message': 'Questions data is required'})

            # Create AssessmentQuestion
            assessment_question = AssessmentQuestion.objects.create(
                department_id=department,
                sop=sop,
                questions_data=questions_data,  # This is a JSON field
                marks=marks,
                created_by=created_by,
                created_at=timezone.now()
            )

            return Response({
                'status': True,
                'message': 'Assessment question created successfully',
                'data': AssessmentQuestionSerializer(assessment_question).data
            })
        except Exception as e:
            return Response({"status": False, 'message': 'Something went wrong', 'error': str(e)})

class AssessmentQuestionUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'assessment_question_id'  # Using a custom lookup field like 'assessment_question_id'

    def update(self, request, *args, **kwargs):
        # Check if the user has the permission to change assessment questions
        if not request.user.has_perm('app_name.change_assessmentquestion'):  # Replace 'app_name' with your app's name
            return Response({"status": False, "message": "You are not authorized to update this assessment question!", "data": []})

        try:
            # Get the assessment question ID from the URL
            assessment_question_id = self.kwargs.get("assessment_question_id")
            
            # Check if the assessment question exists
            if not AssessmentQuestion.objects.filter(id=assessment_question_id).exists():
                return Response({"status": False, "message": "Assessment Question ID not found"})

            # Fetch the assessment question object
            assessment_question = AssessmentQuestion.objects.get(id=assessment_question_id)

            # Get data from the request
            department = request.data.get('department')
            sop = request.data.get('sop')
            questions_data = request.data.get('questions_data')
            marks = request.data.get('marks')

            # Update the assessment question details if provided
            if department:
                assessment_question.department_id = department
            if sop:
                assessment_question.sop = sop
            if questions_data:
                assessment_question.questions_data = questions_data  # Updating the JSON field
            if marks:
                assessment_question.marks = marks
            
            # Save the updated assessment question
            assessment_question.save()

            return Response({
                "status": True,
                "message": "Assessment question updated successfully",
                "data": AssessmentQuestionSerializer(assessment_question).data
            })
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})


class MethodologyCreateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MethodologySerializer
    queryset = Methodology.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['methodology_name','created_at']
    search_fields = ['methodology_name', 'created_by__full_name']

    def create(self, request, *args, **kwargs):
        try:
            methodology_name = request.data.get('methodology_name')
            created_by = self.request.user

            # Validation
            if not methodology_name:
                return Response({'status': False, 'message': 'Methodology name is required'})

            # Create Methodology
            methodology = Methodology.objects.create(
                methodology_name=methodology_name,
                created_by=created_by
            )

            serializer = MethodologySerializer(methodology)
            data = serializer.data
            return Response({
                'status': True,
                'message': 'Methodology created successfully',
                'data': data
            })
        except Exception as e:
            return Response({"status": False, 'message': 'Something went wrong', 'error': str(e)})
        
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = MethodologySerializer(queryset, many=True)
            data = serializer.data
            return Response({"status": True,"message": "Methodologies fetched successfully","data": data})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})
        
class MethodologyUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'methodology_id'  # Using a custom lookup field like 'methodology_id'

    def update(self, request, *args, **kwargs):
        # Check if the user has the permission to change methodologies
        # if not request.user.has_perm('lms_module.change_methodology'):
        #     return Response({"status": False, "message": "You are not authorized to update this methodology!", "data": []})
        try:
            # Get the methodology ID from the URL
            methodology_id = self.kwargs.get("methodology_id")
            
            # Check if the methodology exists
            if not Methodology.objects.filter(id=methodology_id).exists():
                return Response({"status": False, "message": "Methodology ID not found"})

            methodology = Methodology.objects.get(id=methodology_id)
            methodology_name = request.data.get('methodology_name')

            if methodology_name:
                methodology.methodology_name = methodology_name

            methodology.save()
            serializer = MethodologySerializer(methodology)
            data = serializer.data
            return Response({
                "status": True,
                "message": "Methodology updated successfully",
                "data": data
            })
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})
        
    def destroy(self, request, *args, **kwargs):
        # Check if the user has the permission to delete methodologies
        # if not request.user.has_perm('lms_module.delete_methodology'):
        #     return Response({"status": False, "message": "You are not authorized to delete this methodology!", "data": []})
        try:
            # Get the methodology ID from the URL
            methodology_id = self.kwargs.get("methodology_id")
            
            if not Methodology.objects.filter(id=methodology_id).exists():
                return Response({"status": False, "message": "Methodology ID not found"})

            Methodology.objects.filter(id=methodology_id).delete()
            return Response({"status": True, "message": "Methodology deleted successfully"})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})
        

class TrainingTypeCreateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TrainingTypeSerializer
    queryset = TrainingType.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['training_type_name','created_at']
    search_fields = ['training_type_name', 'created_by__full_name']

    def create(self, request, *args, **kwargs):
        try:
            training_type_name = request.data.get('training_type_name')
            created_by = self.request.user

            # Validation
            if not training_type_name:
                return Response({'status': False, 'message': 'Training type name is required'})

            # Create Training Type
            training_type = TrainingType.objects.create(
                training_type_name=training_type_name,
                created_by=created_by
            )

            serializer = TrainingTypeSerializer(training_type)
            data = serializer.data
            return Response({
                'status': True,
                'message': 'Training type created successfully',
                'data': data
            })
        except Exception as e:
            return Response({"status": False, 'message': 'Something went wrong', 'error': str(e)})
        
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = TrainingTypeSerializer(queryset, many=True)
            data = serializer.data
            return Response({"status": True,"message": "Training types fetched successfully","data": data})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})
        

class TrainingTypeUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'training_type_id'  # Using a custom lookup field like 'training_type_id'

    def update(self, request, *args, **kwargs):
        try:
            # Get the training type ID from the URL
            training_type_id = self.kwargs.get("training_type_id")
            
            # Check if the training type exists
            if not TrainingType.objects.filter(id=training_type_id).exists():
                return Response({"status": False, "message": "Training type ID not found"})

            training_type = TrainingType.objects.get(id=training_type_id)
            training_type_name = request.data.get('training_type_name')

            if training_type_name:
                training_type.training_type_name = training_type_name

            training_type.save()
            serializer = TrainingTypeSerializer(training_type)
            data = serializer.data
            return Response({
                "status": True,
                "message": "Training type updated successfully",
                "data": data
            })
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})
        
    def destroy(self, request, *args, **kwargs):
        # Check if the user has the permission to delete training types
        # if not request.user.has_perm('lms_module.delete_trainingtype'):
        #     return Response({"status": False, "message": "You are not authorized to delete this training type!", "data": []})
        try:
            # Get the training type ID from the URL
            training_type_id = self.kwargs.get("training_type_id")
            
            if not TrainingType.objects.filter(id=training_type_id).exists():
                return Response({"status": False, "message": "Training type ID not found"})

            TrainingType.objects.filter(id=training_type_id).delete()
            return Response({"status": True, "message": "Training type deleted successfully"})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})
        

class TrainingCreateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TrainingCreateSerializer
    queryset = TrainingCreate.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['training_name','created_at']
    search_fields = ['training_name', 'created_by__full_name']

    def create(self, request, *args, **kwargs):
        try:
            plant = request.data.get('plant')
            training_type = request.data.get('training_type')
            training_number = request.data.get('training_number')
            training_name = request.data.get('training_name')
            training_version = request.data.get('training_version')
            refresher_time = request.data.get('refresher_time')
            training_document = request.data.get('training_document')
            schedule_date = request.data.get('schedule_date')
            methodology = request.data.get('methodology')

            created_by = self.request.user

            # Validation
            if not plant:
                return Response({'status': False, 'message': 'Plant is required'})
            if not training_type:
                return Response({'status': False, 'message': 'Training type is required'})
            if not training_number:
                return Response({'status': False, 'message': 'Training number is required'})
            if not training_name:
                return Response({'status': False, 'message': 'Training name is required'})
            if not training_version:
                return Response({'status': False, 'message': 'Training version is required'})
            if not refresher_time:
                return Response({'status': False, 'message': 'Refresher time is required'})
            if not training_document:
                return Response({'status': False, 'message': 'Training document is required'})
            if not methodology:
                return Response({'status': False, 'message': 'Methodology is required'})

            try:
                plant = Plant.objects.get(id=plant)
            except Plant.DoesNotExist:
                return Response({'status': False, 'message': 'Plant not found'})
            
            try:
                training_type = TrainingType.objects.get(id=training_type)
            except TrainingType.DoesNotExist:
                return Response({'status': False, 'message': 'Traing type not found'})

            # Generate the file path for saving the document
            document_path = get_training_document_upload_path(training_document.name)
            file_path = os.path.join(settings.MEDIA_ROOT, document_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Write the document to the generated file path
            with open(file_path, 'wb') as destination:
                for chunk in training_document.chunks():
                    destination.write(chunk)

            # Create Training
            training = TrainingCreate.objects.create(
                plant=plant,
                training_type=training_type,
                training_number=training_number,
                training_name=training_name,
                training_version=training_version,
                refresher_time=refresher_time,
                training_document=training_document,
                created_by=created_by,
                schedule_date=schedule_date
            )
            
            if methodology:
                training.methodology.add(*methodology)

            # serializer = TrainingCreateSerializer(training, context = {'request': request})
            # data = serializer.data
            return Response({"status": True,"message": "Training created successfully"})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})
        

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = TrainingCreateSerializer(queryset, many=True, context = {'request': request})
            data = serializer.data
            return Response({"status": True,"message": "Training list fetched successfully","data": data})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})
        


class TrainingUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TrainingCreateSerializer
    queryset = TrainingCreate.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['training_name', 'created_at']
    search_fields = ['training_name', 'created_by__full_name']
    lookup_field = 'training_id'

    # Override the default `update` method provided by ModelViewSet
    def update(self, request, *args, **kwargs):
        try:
            training_id = self.kwargs.get("training_id")

            training = TrainingCreate.objects.get(id=training_id)
            if not training:
                return Response({"status": False, "message": "Training ID not found", "data": []})
            
            plant = request.data.get('plant')
            training_type = request.data.get('training_type')
            training_number = request.data.get('training_number')
            training_name = request.data.get('training_name')
            training_version = request.data.get('training_version')
            refresher_time = request.data.get('refresher_time')
            training_document = request.FILES.get('training_document')  # Use request.FILES for uploaded files
            methodology = request.data.get('methodology')

            if training_name:
                training.training_name = training_name
            if training_version:
                training.training_version = training_version
            if refresher_time:
                training.refresher_time = refresher_time
            if plant:
                training.plant = plant
            if training_type:
                training.training_type = training_type
            if training_number:
                training.training_number = training_number

            training.training_updated_at = timezone.now()

            if training_document:
                document_path = get_training_document_upload_path(training_document.name)
                file_path = os.path.join(settings.MEDIA_ROOT, document_path)

                with open(file_path, 'wb') as destination:
                    for chunk in training_document.chunks():
                        destination.write(chunk)

                training.training_document = document_path

            if methodology:
                training.methodology.set(methodology)

            training.save()

            serializer = TrainingCreateSerializer(training, context={'request': request})
            return Response({
                "status": True,
                "message": "Training updated successfully",
                "data": serializer.data
            })

        except TrainingCreate.DoesNotExist:
            return Response({"status": False, "message": "Training not found", "data": []})
        except Exception as e:
            return Response({"status": False, "message": f"Something went wrong: {str(e)}", "data": []})

class TrainingSectionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TrainingSectionSerializer
    queryset = TrainingSection.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['training']

    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            training_id = request.data.get('training_id')
            training = TrainingCreate.objects.get(id=training_id)
            if not training:
                return Response({"status": False, "message": "Training ID not found", "data": []})
            
            section_name = request.data.get('section_name')
            section_description = request.data.get('section_description')
            section_order = request.data.get('section_order')
            if not section_name:
                return Response({"status": False, "message": "Section name is required", "data": []})
            if section_order is not None:
                section_order = str(section_order)

            training_section = TrainingSection.objects.create(
                training=training,
                section_name=section_name,
                section_description=section_description,
                section_order=section_order,
                created_by=user
            )

            serializer = TrainingSectionSerializer(training_section, context = {'request': request})
            data = serializer.data
            return Response({"status": True,"message": "Training section created successfully","data": data})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})
        

    def list(self, request, *args, **kwargs):
        try:
            training_id = self.kwargs.get("training_id")
            if not training_id:
                return Response({"status": False, "message": "Training ID is required", "data": []})
            
            try:
                training = TrainingCreate.objects.get(id=training_id)
            except TrainingCreate.DoesNotExist:
                return Response({"status": False, "message": "Training ID not found", "data": []})
            
            queryset = self.filter_queryset(self.get_queryset().filter(training=training))
            serializer = TrainingSectionSerializer(queryset, many=True, context = {'request': request})
            data = serializer.data
            return Response({"status": True,"message": "Training section list fetched successfully","data": data})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})
        

class TrainingSectionUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TrainingSectionSerializer
    queryset = TrainingSection.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['training']

    def update(self, request, *args, **kwargs):
        try:
            user = self.request.user
            section_id = self.kwargs.get("section_id")
            if not section_id:
                return Response({"status": False, "message": "Section ID is required", "data": []})
            
            try:
                section = TrainingSection.objects.get(id=section_id)
            except TrainingSection.DoesNotExist:
                return Response({"status": False, "message": "Section ID not found", "data": []})
            
            section_name = request.data.get('section_name', section.section_name)
            section_description = request.data.get('section_description', section.section_description)
            section_order = request.data.get('section_order', section.section_order)
            reason_for_update = request.data.get('reason_for_update', section.reason_for_update)
            training_section_active_status = request.data.get('training_section_active_status', section.training_section_active_status)

            if section_order is not None:
                section_order = str(section_order)

            if section_name:
                section.section_name = section_name
            if section_description:
                section.section_description = section_description
            if section_order:
                section.section_order = section_order
            if reason_for_update:
                section.reason_for_update = reason_for_update

            if training_section_active_status is not None:
                if isinstance(training_section_active_status, bool):
                    section.training_section_active_status = training_section_active_status
                else:
                    return Response({"status": False, "message": "Invalid value for 'training_section_active_status'. It must be a boolean value (True/False).", "data": []})

            section.updated_by = user
            section.save()

            serializer = TrainingSectionSerializer(section, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Training section updated successfully", "data": data})

        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "data": []})
        


    def destroy(self, request, *args, **kwargs):
        try:
            section_id = self.kwargs.get("section_id")
            if not section_id:
                return Response({"status": False, "message": "Section ID is required", "data": []})
            
            try:
                section = TrainingSection.objects.get(id=section_id)
            except TrainingSection.DoesNotExist:
                return Response({"status": False, "message": "Section ID not found", "data": []})
            
            section.delete()
            return Response({"status": True, "message": "Training section deleted successfully", "data": []})

        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "data": []})
                


class TrainingMaterialCreateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TrainingMaterialSerializer
    queryset = TrainingMaterial.objects.all().order_by('-material_created_at')
    
    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user

            section_ids = request.data.get('section_ids',[])
            if not section_ids:
                return Response({"status": False, "message": "Section IDs are required", "data": []})

            sections = TrainingSection.objects.filter(id__in=section_ids)
            if sections.count() != len(section_ids):
                return Response({"status": False, "message": "Some section IDs are invalid", "data": []})

            material_title = request.data.get('material_title')
            material_type = request.data.get('material_type')
            material_file = request.FILES.get('material_file')
            minimum_reading_time = request.data.get('minimum_reading_time')

            if not material_title:
                return Response({"status": False, "message": "Material title is required", "data": []})
            if not material_type:
                return Response({"status": False, "message": "Material type is required", "data": []})
            if material_type not in dict(TrainingMaterial.MATERIAL_CHOICES).keys():
                return Response({"status": False, "message": "Invalid material type", "data": []})
            if not material_file:
                return Response({"status": False, "message": "Material file is required", "data": []})

            training_material = TrainingMaterial.objects.create(
                material_title=material_title,
                material_type=material_type,
                material_file=material_file,
                minimum_reading_time=minimum_reading_time,
                created_by=user,
                material_created_at = timezone.now()
            )
            training_material.section.set(sections)
            training_material.save()

            # Serialize and return the response
            serializer = TrainingMaterialSerializer(training_material, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Training material created successfully", "data": data})

        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e), "data": []})
        

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = TrainingMaterialSerializer(queryset, many=True, context = {'request': request})
            data = serializer.data
            return Response({"status": True,"message": "Training material list fetched successfully","data": data})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})
        

class TrainingMaterialUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TrainingMaterialSerializer
    queryset = TrainingMaterial.objects.all().order_by('-material_created_at')
    
    def update(self, request, *args, **kwargs):
        try:
            user = self.request.user

            section_id = request.data.get('section_id')
            if not section_id:
                return Response({"status": False, "message": "Section ID is required", "data": []})

            section = TrainingMaterial.objects.get(id=section_id)
            if not section:
                return Response({"status": False, "message": "Section ID not found", "data": []})

            material_title = request.data.get('material_title', section.material_title)
            material_type = request.data.get('material_type', section.material_type)
            material_file = request.FILES.get('material_file', section.material_file)
            minimum_reading_time = request.data.get('minimum_reading_time', section.minimum_reading_time)

            if material_title:
                section.material_title = material_title
            if material_type:
                section.material_type = material_type
            if material_file:
                section.material_file = material_file
            if minimum_reading_time:
                section.minimum_reading_time = minimum_reading_time
            section.updated_by = user
            section.save()

            serializer = TrainingMaterialSerializer(section, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Training material updated successfully", "data": data})

        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e), "data": []})
        
    def destroy(self, request, *args, **kwargs):
        try:
            section_id = self.kwargs.get('section_id')
            
            try:
                section = TrainingMaterial.objects.get(id=section_id)
            except TrainingMaterial.DoesNotExist:
                return Response({"status": False, "message": "Section ID not found", "data": []})
            
            section.delete()
            return Response({"status": True, "message": "Training material deleted successfully", "data": []})

        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "data": []})

        

class TrainingQuestionCreateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TrainingQuestinSerializer
    queryset = TrainingQuestions.objects.all().order_by('-question_created_at')
    
    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            training = request.data.get('training_id')
            if not training:
                return Response({"status": False, "message": "Training ID is required", "data": []})

            training = TrainingCreate.objects.get(id=training)
            if not training:
                return Response({"status": False, "message": "Training ID not found", "data": []})

            question_type = request.data.get('question_type')
            question_text = request.data.get('question_text')
            options = request.data.get('options', [])
            correct_answer = request.data.get('correct_answer')
            marks = request.data.get('marks')
            language = request.data.get('language')

            if not question_type:
                return Response({"status": False, "message": "Question type is required", "data": []})
            if not question_text:
                return Response({"status": False, "message": "Question text is required", "data": []})
            
            # Validate correct_answer based on question type
            if question_type == 'mcq' and not options:
                return Response({"status": False, "message": "MCQ questions must have options", "data": []})

            if question_type == 'mcq' and correct_answer not in options:
                return Response({"status": False, "message": "MCQ correct answer must be one of the options", "data": []})

            if question_type == 'true_false' and correct_answer not in ['True', 'False']:
                return Response({"status": False, "message": "True/False correct answer must be 'True' or 'False'", "data": []})

            if question_type == 'fill_in_the_blank' and not correct_answer:
                return Response({"status": False, "message": "Fill-in-the-blank questions must have a correct answer", "data": []})

            # File validation for audio and video files (max 25MB)
            audio_file = request.FILES.get('audio_file', None)
            video_file = request.FILES.get('video_file', None)

            if audio_file:
                if audio_file.size > 25 * 1024 * 1024:  # 25MB limit
                    return Response({"status": False, "message": "Audio file size must be less than 25MB.", "data": []})

            if video_file:
                if video_file.size > 25 * 1024 * 1024:  # 25MB limit
                    return Response({"status": False, "message": "Video file size must be less than 25MB.", "data": []})

            # Create the TrainingQuestion instance
            training_question = TrainingQuestions.objects.create(
                training=training,
                question_type=question_type,
                question_text=question_text,
                options=options,
                correct_answer=correct_answer,
                marks=marks,
                language=language,
                created_by=user,
                audio_file=audio_file,
                video_file=video_file,
                question_created_at=timezone.now()
            )

            # Serialize and return the response
            serializer = TrainingQuestinSerializer(training_question, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Training question created successfully", "data": data})

        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e), "data": []})
        

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = TrainingQuestinSerializer(queryset, many=True, context = {'request': request})
            data = serializer.data
            return Response({"status": True,"message": "Training question list fetched successfully","data": data})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})


class TrainingQuestionUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TrainingQuestinSerializer
    queryset = TrainingQuestions.objects.all().order_by('-question_created_at')
    lookup_field = 'training_question_id'

    
    def update(self, request, *args, **kwargs):
        try:
            user = self.request.user
            training_question_id = self.kwargs.get('training_question_id')  # Fix to match the URL
            if not training_question_id:
                return Response({"status": False, "message": "Training question ID is required", "data": []})

            # Fetch the TrainingQuestions object
            section = TrainingQuestions.objects.get(id=training_question_id)
            if not section:
                return Response({"status": False, "message": "Training question ID not found", "data": []})

            # Get data from the request or use existing values (for updates)
            question_type = request.data.get('question_type', section.question_type)
            question_text = request.data.get('question_text', section.question_text)
            options = request.data.get('options', section.options)
            correct_answer = request.data.get('correct_answer', section.correct_answer)
            marks = request.data.get('marks', section.marks)
            language = request.data.get('language', section.language)
            audio_file = request.FILES.get('audio_file', section.audio_file)
            video_file = request.FILES.get('video_file', section.video_file)

            # Validation checks for question_type and other fields
            if not question_type:
                return Response({"status": False, "message": "Question type is required", "data": []})
            if not question_text:
                return Response({"status": False, "message": "Question text is required", "data": []})

            # Additional validation for specific question types
            if question_type == 'mcq' and not options:
                return Response({"status": False, "message": "MCQ questions must have options", "data": []})

            if question_type == 'mcq' and correct_answer not in options:
                return Response({"status": False, "message": "MCQ correct answer must be one of the options", "data": []})

            if question_type == 'true_false' and correct_answer not in ['True', 'False']:
                return Response({"status": False, "message": "True/False correct answer must be 'True' or 'False'", "data": []})

            if question_type == 'fill_in_the_blank' and not correct_answer:
                return Response({"status": False, "message": "Fill-in-the-blank questions must have a correct answer", "data": []})

            # Update the fields of the section
            section.question_type = question_type
            section.question_text = question_text
            section.options = options
            section.correct_answer = correct_answer
            section.marks = marks
            section.language = language

            # Only update the audio or video file if they are provided in the request
            if audio_file:
                section.audio_file = audio_file

            if video_file:
                section.video_file = video_file

            section.updated_by = user
            section.question_updated_at = timezone.now()
            section.save()

            # Serialize and return the updated data
            serializer = TrainingQuestinSerializer(section, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Training question updated successfully", "data": data})

        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e), "data": []})
        

    def destroy(self, request, *args, **kwargs):
        try:
            section_id = self.kwargs.get('section_id')
            
            try:
                section = TrainingQuestions.objects.get(id=section_id)
            except TrainingQuestions.DoesNotExist:
                return Response({"status": False, "message": "Section ID not found", "data": []})
            
            section.delete()
            return Response({"status": True, "message": "Training question deleted successfully", "data": []})

        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "data": []})



class TrainingQuizCreateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TrainingQuizSerializer
    queryset = TrainingQuiz.objects.all().order_by('-created_at')

    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            training_id = request.data.get('training_id')
            quiz_name = request.data.get('name')
            pass_criteria = request.data.get('pass_criteria')
            quiz_time = request.data.get('quiz_time')
            quiz_type = request.data.get('quiz_type')
            total_marks = int(request.data.get('total_marks', 0)) 
            marks_breakdown = request.data.get('marks_breakdown')  # e.g., {'1': 5, '2': 3, '3': 2}
            selected_questions = request.data.get('selected_questions', [])  

            if not all([training_id, quiz_name, pass_criteria, quiz_time, quiz_type, total_marks]):
                return Response({"status": False, "message": "Missing required fields", "data": []})

            try:
                training = TrainingCreate.objects.get(id=training_id)
            except TrainingCreate.DoesNotExist:
                return Response({"status": False, "message": "Training not found", "data": []})

            quiz = TrainingQuiz.objects.create(
                name=quiz_name,
                pass_criteria=pass_criteria,
                quiz_time=quiz_time,
                quiz_type=quiz_type,
                created_by=user,
                training=training,
            )

            total_marks_accumulated = 0  
            total_questions = 0  

            if quiz_type == 'auto':
                
                for marks, count in marks_breakdown.items():
                    marks = int(marks)  
                    count = int(count)  
        
                    questions = TrainingQuestions.objects.filter(
                        training=training,  
                        marks=marks,       
                        status=True         
                    )

                    if len(questions) < count:
                        return Response({"status": False,"message": f"Not enough questions with {marks} marks. Found {len(questions)} questions.","data": []})
                    selected_questions = random.sample(questions, count)

                    potential_marks = total_marks_accumulated + (marks * count)
                    if potential_marks > total_marks:
                        return Response({"status": False,"message": f"Total marks exceeded. The selected questions' marks total {potential_marks}, which exceeds the input total_marks of {total_marks}.","data": []})

                    for question in selected_questions:
                        QuizQuestion.objects.create(quiz=quiz, question=question, marks=marks)

                    total_marks_accumulated += marks * count
                    total_questions += count

            elif quiz_type == 'manual':
                if not selected_questions or not isinstance(selected_questions, list):
                    return Response({
                        "status": False,
                        "message": "You must provide a list of selected questions for manual quiz creation.",
                        "data": []
                    })

                questions = TrainingQuestions.objects.filter(
                    id__in=selected_questions,  
                    training=training,  
                    status=True
                )

                if len(questions) != len(selected_questions):
                    return Response({
                        "status": False,
                        "message": "Some of the selected questions are invalid or inactive.",
                        "data": []
                    })

                for question in questions:
                    if total_marks_accumulated + question.marks > total_marks:
                        return Response({
                            "status": False,
                            "message": f"Adding this question would exceed the total marks. Current total: {total_marks_accumulated}, question marks: {question.marks}",
                            "data": []
                        })
                    QuizQuestion.objects.create(quiz=quiz, question=question, marks=question.marks)
                    total_marks_accumulated += question.marks
                    total_questions += 1

            if total_marks_accumulated != total_marks:
                return Response({
                    "status": False,
                    "message": f"Total marks mismatch. The accumulated marks are {total_marks_accumulated}, but the input total_marks was {total_marks}. Please adjust.",
                    "data": []
                })

            quiz.total_marks = total_marks_accumulated
            quiz.total_questions = total_questions
            quiz.save()

            serializer = TrainingQuizSerializer(quiz, context={'request': request})
            return Response({"status": True, "message": "Quiz created successfully", "data": serializer.data})

        except IntegrityError as e:
            return Response({"status": False, "message": "Database Integrity Error", "error": str(e), "data": []})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e), "data": []})



    def list(self, request, *args, **kwargs):
        try:
            user = self.request.user
            queryset = TrainingQuiz.objects.filter(created_by=user).order_by('-created_at')
            serializer = TrainingQuizSerializer(queryset, many=True, context={'request': request})
            return Response({"status": True, "message": "Quizzes retrieved successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e), "data": []})


class TrainingQuizUpdateView(viewsets.ModelViewSet):
    queryset = TrainingQuiz.objects.all()
    serializer_class = TrainingQuizSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'training_quiz_id'

    def update(self, request, *args, **kwargs):
        try:
            user = self.request.user
            training_quiz_id = self.kwargs.get('training_quiz_id')
            quiz = TrainingQuiz.objects.get(id=training_quiz_id)

            # Check if the quiz status is False user can not update
            if not quiz.status:
                return Response({"status": False, "message": "Quiz is not active", "data": []})

            training_id = request.data.get('training_id', quiz.training.id)
            quiz_name = request.data.get('name', quiz.quiz_name)
            pass_criteria = request.data.get('pass_criteria', quiz.pass_criteria)
            quiz_time = request.data.get('quiz_time', quiz.quiz_time)
            quiz_type = request.data.get('quiz_type', quiz.quiz_type)
            total_marks = int(request.data.get('total_marks', quiz.total_marks)) 
            marks_breakdown = request.data.get('marks_breakdown')  # e.g., {'1': 5, '2': 3, '3': 2}
            selected_questions = request.data.get('selected_questions', [])
            status = request.data.get('status',quiz.status)

            if not all([training_id, quiz_name, pass_criteria, quiz_time, quiz_type, total_marks]):
                return Response({"status": False, "message": "Missing required fields", "data": []})

            try:
                training = TrainingCreate.objects.get(id=training_id)
            except TrainingCreate.DoesNotExist:
                return Response({"status": False, "message": "Training not found", "data": []})

            quiz.training = training
            quiz.quiz_name = quiz_name
            quiz.pass_criteria = pass_criteria
            quiz.quiz_time = quiz_time
            quiz.quiz_type = quiz_type
            quiz.updated_by = user
            quiz.updated_at = timezone.now()
            quiz.total_marks = total_marks  # Update total marks if needed
            quiz.total_questions = 0  # Reset question count, will recalculate later
            if status is not None:
                if isinstance(status,bool):
                    quiz.status = status
                else:
                    return Response({"status": False, "message": "Invalid status value", "data": []})
            
            quiz.save()

            total_marks_accumulated = 0  
            total_questions = 0  

            if quiz_type == 'auto':
                # Handling 'auto' type quizzes
                if marks_breakdown:
                    # Clear existing questions if it's an "auto" quiz
                    old_questions = QuizQuestion.objects.filter(quiz=quiz)

                    for marks, count in marks_breakdown.items():
                        marks = int(marks)  
                        count = int(count)  

                        questions = TrainingQuestions.objects.filter(
                            training=training,  
                            marks=marks,       
                            status=True         
                        )

                        if len(questions) < count:
                            return Response({"status": False, "message": f"Not enough questions with {marks} marks. Found {len(questions)} questions.", "data": []})

                        # Select random questions based on count
                        selected_questions = random.sample(questions, count)

                        potential_marks = total_marks_accumulated + (marks * count)
                        if potential_marks > total_marks:
                            return Response({"status": False, "message": f"Total marks exceeded. The selected questions' marks total {potential_marks}, which exceeds the input total_marks of {total_marks}.", "data": []})

                        # For each selected question, update or add it
                        for question in selected_questions:
                            existing_question = old_questions.filter(question=question).first()
                            if existing_question:
                                # If the question already exists, do nothing, just update marks if needed
                                existing_question.marks = marks  # If you want to update marks, do it here
                                existing_question.save()
                            else:
                                # If the question is new, add it to the quiz
                                QuizQuestion.objects.create(quiz=quiz, question=question, marks=marks)
                            total_marks_accumulated += marks
                            total_questions += 1

            elif quiz_type == 'manual':
                # Handling 'manual' type quizzes
                if selected_questions:
                    questions = TrainingQuestions.objects.filter(
                        id__in=selected_questions,  
                        training=training,  
                        status=True
                    )

                    if len(questions) != len(selected_questions):
                        return Response({
                            "status": False,
                            "message": "Some of the selected questions are invalid or inactive.",
                            "data": []
                        })

                    # Add new or checked questions to the quiz
                    for question in questions:
                        if total_marks_accumulated + question.marks > total_marks:
                            return Response({
                                "status": False,
                                "message": f"Adding this question would exceed the total marks. Current total: {total_marks_accumulated}, question marks: {question.marks}",
                                "data": []
                            })
                        # Add the question if it's not already in the quiz
                        if not QuizQuestion.objects.filter(quiz=quiz, question=question).exists():
                            QuizQuestion.objects.create(quiz=quiz, question=question, marks=question.marks)
                            total_marks_accumulated += question.marks
                            total_questions += 1

                    # Remove unchecked questions
                    existing_quiz_questions = QuizQuestion.objects.filter(quiz=quiz)
                    for quiz_question in existing_quiz_questions:
                        # If a question is not selected anymore, remove it from the quiz
                        if quiz_question.question.id not in selected_questions:
                            quiz_question.delete()

            if total_marks_accumulated != total_marks:
                return Response({
                    "status": False,
                    "message": f"Total marks mismatch. The accumulated marks are {total_marks_accumulated}, but the input total_marks was {total_marks}. Please adjust.",
                    "data": []
                })

            quiz.total_marks = total_marks_accumulated
            quiz.total_questions = total_questions
            quiz.save()

            serializer = TrainingQuizSerializer(quiz, context={'request': request})
            return Response({"status": True, "message": "Quiz updated successfully", "data": serializer.data})

        except TrainingQuiz.DoesNotExist:
            return Response({"status": False, "message": "Quiz not found", "data": []})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e), "data": []})

    def destroy(self, request, *args, **kwargs):
        try:
            training_quiz_id = self.kwargs.get("training_quiz_id")
            quiz = TrainingQuiz.objects.get(id=training_quiz_id)
            quiz.delete()
            return Response({"status": True, "message": "Quiz deleted successfully", "data": []})
        except TrainingQuiz.DoesNotExist:
            return Response({"status": False, "message": "Quiz not found", "data": []})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e), "data": []})
    
        
        
class InductionCreateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InductionSerializer
    queryset = Induction.objects.all().order_by('-id')

    def create(self, request, *args, **kwargs):
        try:
            plant = request.data.get('plant')
            induction_name = request.data.get('induction_name')
            trainings = request.data.get('trainings', [])

            # Validation
            if not plant:
                return Response({'status': False, 'message': 'Plant is required'})
            if not induction_name:
                return Response({'status': False, 'message': 'Induction name is required'})
            
            # Create Induction
            induction = Induction.objects.create(
                plant_id=plant,
                induction_name=induction_name
            )

            if trainings:
                induction.trainings.add(*trainings)

            serializer = InductionSerializer(induction, context={'request': request})
            return Response({"status": True, "message": "Induction created successfully", "data": serializer.data})

        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})
        
    def list(self, request):
        queryset = Induction.objects.all().order_by('-id')
        
        try:
            if queryset.exists():
                serializer = InductionSerializer(queryset, many=True)
                return Response({
                    "status": True,
                    "message": "Induction fetched successfully",
                    "total": queryset.count(),
                    "data": serializer.data
                })
            else:
                return Response({
                    "status": True,
                    "message": "No induction found",
                    "total": 0,
                    "data": []
                })
        except Exception as e:
            return Response({"status": False, 'message': 'Something went wrong', 'error': str(e)})    

class InductionUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InductionSerializer
    queryset = Induction.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        try:
            induction = self.get_object()
            induction_name = request.data.get('induction_name')
            plant = request.data.get('plant')
            trainings = request.data.get('trainings', [])

            if induction_name:
                induction.induction_name = induction_name
            if plant:
                induction.plant_id = plant

            induction.save()

            if trainings:
                induction.trainings.set(trainings)

            serializer = InductionSerializer(induction, context={'request': request})
            return Response({"status": True, "message": "Induction updated successfully", "data": serializer.data})

        except Exception as e:
            return Response({"status": False, "message": f"Something went wrong: {str(e)}", "data": []})
          
           
    def destroy(self, request, *args, **kwargs):
        try:
            induction = self.get_object()
            induction.delete()
            return Response({"status": True, "message": "Induction deleted successfully"})
        except Exception as e:
            return Response({"status": False, "message": f"Something went wrong: {str(e)}"})

class InductionDesignationCreateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InductionDesignationSerializer
    queryset = InductionDesignation.objects.all().order_by('-id')

    def create(self, request, *args, **kwargs):
        try:
            induction_designation_name = request.data.get('induction_designation_name')
            designation_code = request.data.get('designation_code')
            induction_id = request.data.get('induction')

            # Validation
            if not induction_designation_name:
                return Response({'status': False, 'message': 'Induction Designation Name is required'})
            if not designation_code:
                return Response({'status': False, 'message': 'Designation Code is required'})
            if not induction_id:
                return Response({'status': False, 'message': 'Induction ID is required'})

            induction_designation = InductionDesignation.objects.create(
                induction_designation_name=induction_designation_name,
                designation_code=designation_code,
                induction_id=induction_id,
                created_by=request.user
            )

            serializer = self.get_serializer(induction_designation)
            return Response({"status": True, "message": "Induction Designation created successfully", "data": serializer.data})

        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})
        
    def list(self, request):
        queryset = InductionDesignation.objects.all().order_by('-id')
        
        try:
            if queryset.exists():
                serializer = InductionDesignationSerializer(queryset, many=True)
                return Response({
                    "status": True,
                    "message": "Induction designations fetched successfully",
                    "total": queryset.count(),
                    "data": serializer.data
                })
            else:
                return Response({
                    "status": True,
                    "message": "No induction designation found",
                    "total": 0,
                    "data": []
                })
        except Exception as e:
            return Response({"status": False, 'message': 'Something went wrong', 'error': str(e)})      

class InductionDesignationUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InductionDesignationSerializer
    queryset = InductionDesignation.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        try:
            induction_designation = self.get_object()
            induction_designation_name = request.data.get('induction_designation_name')
            designation_code = request.data.get('designation_code')
            induction_id = request.data.get('induction')

            if induction_designation_name:
                induction_designation.induction_designation_name = induction_designation_name
            if designation_code:
                induction_designation.designation_code = designation_code
            if induction_id:
                induction_designation.induction_id = induction_id

            induction_designation.save()
            serializer = self.get_serializer(induction_designation)
            return Response({"status": True, "message": "Induction Designation updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status": False, "message": f"Something went wrong: {str(e)}"})

    def destroy(self, request, *args, **kwargs):
        # Check if the user has permission to delete InductionDesignations
        # if not request.user.has_perm('your_app.delete_inductiondesignation'):
        #     return Response({"status": False, "message": "You are not authorized to delete this designation!"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            # Get the InductionDesignation ID from the URL
            induction_id = self.kwargs.get("id")
            
            # Check if the InductionDesignation exists
            if not InductionDesignation.objects.filter(id=induction_id).exists():
                return Response({"status": False, "message": "InductionDesignation ID not found"})

            # Delete the InductionDesignation
            InductionDesignation.objects.filter(id=induction_id).delete()
            return Response({"status": True, "message": "InductionDesignation deleted successfully"})
        
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})       




class ClassroomTrainingCreateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClassroomTrainingSerializer
    queryset = ClassroomTraining.objects.all().order_by('-created_at')

    def create(self, request, *args, **kwargs):
        try:
            title = request.data.get('title')
            department_or_employee = request.data.get('department_or_employee')
            training_type = request.data.get('classroom_training_type')
            description = request.data.get('description')
            sop = request.data.get('sop')
            start_date = request.data.get('start_date')
            start_time = request.data.get('start_time')
            end_time = request.data.get('end_time')
            document = request.data.get('document')
            status = request.data.get('status', 'assigned')
            created_by = request.user.id

            # Validation
            if not title or not department_or_employee or not training_type or not description:
                return Response({'status': False, 'message': 'All fields are required.'})

            # Create Classroom Training
            classroom_training = ClassroomTraining.objects.create(
                title=title,
                department_or_employee_id=department_or_employee,
                classroom_training_type=training_type,
                description=description,
                sop=sop,
                start_date=start_date,
                start_time=start_time,
                end_time=end_time,
                created_by_id=created_by,
                status=status
            )

            if document:
                classroom_training.document = document
                classroom_training.save()

            serializer = ClassroomTrainingSerializer(classroom_training, context={'request': request})
            return Response({
                "status": True,
                "message": "Classroom training created successfully",
                "data": serializer.data
            })

        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})


    def mark_completed(self, request, *args, **kwargs):
        try:
            # Get the classroom training object
            classroom_training = self.get_object()
            if classroom_training.classroom_training_type == "assessment":
                # Check if all users have provided assessment results
                users = classroom_training.department_or_employee.users.all()  # Assuming `users` is a related field
                missing_assessment = []

                for user in users:
                    if not user.assessment_result:  # Assuming `assessment_result` is the field on the user model
                        missing_assessment.append(user.username)

                if missing_assessment:
                    return Response({
                        "status": False,
                        "message": f"Please provide assessment results for the following users: {', '.join(missing_assessment)}"
                    })

            # If no missing assessment or no assessment type, change status to completed
            classroom_training.status = 'completed'
            classroom_training.save()

            return Response({
                "status": True,
                "message": "Classroom training status updated to completed successfully"
            })
        except Exception as e:
            return Response({
                "status": False,
                "message": f"Something went wrong: {str(e)}"
            })


class ClassroomTrainingUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClassroomTrainingSerializer
    queryset = ClassroomTraining.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        try:
            classroom_training = self.get_object()
            training_type = request.data.get('classroom_training_type')
            title = request.data.get('title')
            department_or_employee = request.data.get('department_or_employee')
            description = request.data.get('description')
            sop = request.data.get('sop')
            start_date = request.data.get('start_date')
            start_time = request.data.get('start_time')
            end_time = request.data.get('end_time')
            status = request.data.get('status')
            acknowledged_by_employee = request.data.get('acknowledged_by_employee')

            # Updating fields
            if training_type: classroom_training.classroom_training_type = training_type
            if title: classroom_training.title = title
            if department_or_employee: classroom_training.department_or_employee_id = department_or_employee
            if description: classroom_training.description = description
            if sop: classroom_training.sop = sop
            if start_date: classroom_training.start_date = start_date
            if start_time: classroom_training.start_time = start_time
            if end_time: classroom_training.end_time = end_time
            if status: classroom_training.status = status
            if acknowledged_by_employee is not None:
                classroom_training.acknowledged_by_employee = acknowledged_by_employee

            classroom_training.save()
            serializer = ClassroomTrainingSerializer(classroom_training, context={'request': request})
            return Response({"status": True, "message": "Classroom training updated successfully", "data": serializer.data})

        except Exception as e:
            return Response({"status": False, "message": f"Something went wrong: {str(e)}", "data": []})

    def destroy(self, request, *args, **kwargs):
        try:
            classroom_training = self.get_object()
            classroom_training.delete()
            return Response({"status": True, "message": "Classroom training deleted successfully"})
        except Exception as e:
            return Response({"status": False, "message": f"Something went wrong: {str(e)}"})
        
class TrainingListViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TrainingListSerializer
    queryset = TrainingCreate.objects.all()

    def list(self, request, *args, **kwargs):
        plant_id = request.data.get('plant')
        training_type_id = request.data.get('type')
        training_number = request.data.get('training_number')

        filters = Q()
        if plant_id:
            filters &= Q(plant_id=plant_id)
        if training_type_id:
            filters &= Q(training_type_id=training_type_id)
        if training_number:
            filters &= Q(training_number=training_number)

        trainings = self.queryset.filter(filters)

        serializer = self.get_serializer(trainings, many=True)
        return Response({
            "status": True,
            "message": "Training data fetched successfully",
            "data": serializer.data
        })



class TrainingMatrixAssignUserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = TrainingMatrix.objects.all()
    serializer_class = TrainingMatrixAssignUserSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user
        training_create_id = request.data.get('training_create_id')
        user_ids = request.data.get('user_ids', [])
        training_duration = request.data.get('training_duration', None)
        evaluation_status = request.data.get('evaluation_status', None)
        assigned_role_id = request.data.get('assigned_role', None)
        due_reason = request.data.get('due_reason', None)

        if not training_create_id:
            return Response({"status": False,"message": "TrainingCreate ID not provided.","data": []})

        try:
            training_create_instance = TrainingCreate.objects.get(id=training_create_id)
        except TrainingCreate.DoesNotExist:
            return Response({
                "status": False,"message": "TrainingCreate instance not found.","data": []})

        if not user_ids:
            return Response({"status": False,"message": "User IDs not provided.","data": []})

        users = CustomUser.objects.filter(id__in=user_ids)
        if users.count() != len(user_ids):
            return Response({"status": False,"message": "Invalid user IDs.","data": []})

        assigned_role = None
        if assigned_role_id:
            try:
                assigned_role = JobRole.objects.get(id=assigned_role_id)
            except JobRole.DoesNotExist:
                return Response({
                    "status": False,"message": "Assigned role not found.","data": []})

        training_matrix = TrainingMatrix.objects.create(
            training=training_create_instance,
            assigned_by=user,
            training_duration=training_duration,
            evaluation_status=evaluation_status,
            assigned_role=assigned_role,
            due_reason=due_reason
        )

        training_matrix.assigned_user.set(users)
        training_matrix.save()

        serializer = TrainingMatrixAssignUserSerializer(training_matrix)

        return Response({"status": True,"message": "Training matrix created and users assigned successfully.","data": serializer.data})

    
class JobroleListingViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetJobRoleSerializer

    def list(self, request, *args, **kwargs):
        plant_id = request.data.get('plant')
        department_id = request.data.get('department')
        area_id = request.data.get('area')

        job_roles = JobRole.objects.all()

        if plant_id:
            job_roles = job_roles.filter(plant_id=plant_id)
        if department_id:
            job_roles = job_roles.filter(department_id=department_id)
        if area_id:
            job_roles = job_roles.filter(area_id=area_id)

        job_role_serializer = GetJobRoleSerializer(job_roles, many=True)

        return Response({
            "status": True,
            "message": "Training and job role data fetched successfully",
            "data": {
                "job_roles": job_role_serializer.data
                }
        })


class TrainingAssignViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = TrainingCreate.objects.all()
    lookup_field = 'training_id'  

    def update(self, request, *args, **kwargs):
        try:
            training_id = self.kwargs.get("training_id")

            training_instance = TrainingCreate.objects.filter(id=training_id).first()
            if not training_instance:
                return Response({"status": False, "message": "Training ID not found"})

            job_role_ids = request.data.get('job_role_ids', [])
            if not isinstance(job_role_ids, list):
                return Response({"status": False, "message": "Job role IDs should be a list"})

            valid_job_roles = JobRole.objects.filter(id__in=job_role_ids)
            if len(valid_job_roles) != len(job_role_ids):
                return Response({
                    "status": False,
                    "message": "Some Job Role IDs are invalid"
                })

            training_instance.job_roles.set(valid_job_roles)
            training_instance.save()

            return Response({
                "status": True,
                "message": "Training updated successfully",
            })
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})


class JobroleListingapiViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetJobRoleSerializer

    def list(self, request, *args, **kwargs):
        plant_id = request.data.get('plant')
        department_id = request.data.get('department')
        area_id = request.data.get('area')
        job_role_name = request.data.get('job_role_name')

        job_roles = JobRole.objects.all()

        if plant_id:
            job_roles = job_roles.filter(plant_id=plant_id)
        if department_id:
            job_roles = job_roles.filter(department_id=department_id)
        if area_id:
            job_roles = job_roles.filter(area_id=area_id)
        if job_role_name:
            job_roles = job_roles.filter(job_role_name__icontains=job_role_name)

        job_role_serializer = self.serializer_class(job_roles, many=True)

        return Response({
            "status": True,
            "message": "Training and job role data fetched successfully",
            "data": {
                "job_roles": job_role_serializer.data
            }
        })


class TrainingListingViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TrainingSerializer

    def list(self, request, *args, **kwargs):
        training_type_id = request.data.get("training_type")

        trainings = TrainingCreate.objects.all()

        if training_type_id:
            trainings = trainings.filter(training_type_id=training_type_id)

        # Serialize the data
        training_serializer = self.serializer_class(trainings, many=True)

        # Return the response
        return Response({
            "status": True,
            "message": "Training data fetched successfully",
            "data": training_serializer.data
        })


