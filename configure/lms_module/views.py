from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import permissions

class DepartmentAddView(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
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
        if not request.user.has_perm('dashboard_app.change_departmentmaster'):
            return Response({"status": False, "message": "You are not authorized to update department!", "data": []})
    
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








