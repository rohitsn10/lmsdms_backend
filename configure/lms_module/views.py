from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import permissions
from user_profile.function_call import *
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
                created_by=created_by
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
