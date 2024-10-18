from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.response import Response
from .models import *
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from rest_framework import permissions

class CustomPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'  # Allow users to set page size
    max_page_size = 100  # Maximum page size

class WorkFlowViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WorkFlowSerializer
    queryset = WorkFlowModel.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['workflow_name', 'workflow_description']
    ordering_fields = ['workflow_name', 'created_at']

    def create(self, request):
        try:
            workflow_name = request.data.get('workflow_name')
            workflow_description = request.data.get('workflow_description', '')
            is_active = request.data.get('is_active', True)

            if not workflow_name:
                return Response({'status': False, 'message': 'Workflow name is required'})

            workflow_obj = WorkFlowModel.objects.create(
                workflow_name=workflow_name,
                workflow_description=workflow_description,
                # is_active=is_active
            )
            serializer = WorkFlowSerializer(workflow_obj)
            return Response({'status': True, 'message': 'Workflow created successfully', 'data': serializer.data})
        except Exception as e:
            return Response({'status': False, 'message': 'Something went wrong', 'error': str(e)})

    # List all workflows
    def list(self, request):
        queryset = WorkFlowModel.objects.all().order_by('-id')
        
        try:
            if queryset.exists():
                serializer = WorkFlowSerializer(queryset, many=True)
                return Response({
                    "status": True,
                    "message": "Workflows fetched successfully",
                    'total': queryset.count(),
                    'data': serializer.data
                })
            else:
                return Response({
                    "status": True,
                    "message": "No Workflow found",
                    "total": 0,
                    "data": []
                })
        except Exception as e:
            return Response({"status": False, 'message': 'Something went wrong', 'error': str(e)})


class WorkFlowUpdateSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WorkFlowSerializer
    lookup_field = 'workflow_id'

    def update(self, request, *args, **kwargs):
        if not request.user.has_perm('dashboard_app.change_departmentmaster'):
            return Response({"status": False, "message": "You are not authorized to update department!", "data": []})
    
        try:
            workflow_id = self.kwargs.get("workflow_id")
            workflow_name = request.data.get('workflow_name')
            workflow_description = request.data.get('workflow_description')
    
            workflow_object = WorkFlowModel.objects.get(id=workflow_id)
            if workflow_name:
                workflow_object.workflow_name = workflow_name
            if workflow_description:
                workflow_object.workflow_description = workflow_description
            workflow_object.save()
    
            return Response({'status': True, 'message': 'Workflow updated successfully'})
        except WorkFlowModel.DoesNotExist:
            return Response({'status': False, 'message': 'Workflow not found'})
        except Exception as e:
            return Response({'status': False, 'message': 'Something went wrong', 'error': str(e)})
        
    def destroy(self, request, *args, **kwargs):
        try:
            workflow_id = request.data.get('workflow_id')   
            if not WorkFlowModel.objects.filter(id=workflow_id):
                return Response({"status":False, "message":"Workflow id not found"})
                     
            department_object = WorkFlowModel.objects.get(id=workflow_id)
            department_object.delete()
            return Response({"status":True, "message":"Workflow deleted succesfully"})
        except Exception as e:
                return Response({"status": False,'message': 'Something went wrong','error': str(e)})



class DocumentTypeCreateViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentTypeSerializer
    queryset = DocumentType.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            document_name = request.data.get('document_name')
            if not document_name:
                return Response({"status": False, "message": "Document name is required", "data": []})
            document_type = DocumentType.objects.create(user = user, document_name=document_name)
            serializer = DocumentTypeSerializer(document_type)
            return Response({"status": True, "message": "Document type created successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
    def list(self, request, *args, **kwargs):
        try:
            queryset = DocumentType.objects.all()
            serializer = DocumentTypeSerializer(queryset, many=True)
            return Response({"status": True, "message": "Document type list fetched successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
        
class PrintRequest(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = PrintRequest.objects.all().order_by('-id')

    def create(self, request):
        try:
            user = self.request.user
            no_of_print = request.data.get('no_of_print')
            issue_type = request.data.get('issue_type')
            reason_for_print = request.data.get('reason_for_print')

            if not no_of_print:
                return Response({'status': False, 'message': 'NO of print is required'})
            if not issue_type:
                return Response({'status': False, 'message': 'Issue type is required'})
            if not reason_for_print:
                return Response({'status': False, 'message': 'Reason is required'})

            printrequest_obj = PrintRequest.objects.create(
                user = user,
                no_of_print=no_of_print,
                issue_type=issue_type,
                reason_for_print=reason_for_print
            )
            return Response({'status': True, 'message': 'Print requested successfully'})
        except Exception as e:
            return Response({'status': False, 'message': 'Something went wrong', 'error': str(e)})
        

class PrintApproval(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = PrintRequestApproval.objects.all().order_by('-id')

    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            print_request_id = request.data.get('print_request_id')
            no_of_request_by_admin = request.data.get('no_of_request_by_admin')
            status = request.data.get('status')

            # Validate that the print_request_id is provided
            if not print_request_id:
                return Response({'status': False, 'message': 'Print request ID is required'})
            
            # Fetch the associated PrintRequest object
            try:
                print_request = PrintRequest.objects.get(id=print_request_id)
            except PrintRequest.DoesNotExist:
                return Response({'status': False, 'message': 'Invalid Print Request ID'})
            
            # Validate the status field
            if not status or status not in ['approved', 'rejected']:
                return Response({'status': False, 'message': 'Status must be either "approved" or "rejected"'})
            
            # If status is 'approved', no_of_request_by_admin is mandatory
            if status == 'approved':
                if not no_of_request_by_admin:
                    return Response({'status': False, 'message': 'No of request by admin is required when approving'})
                
                # Ensure no_of_request_by_admin does not exceed no_of_print from PrintRequest
                if int(no_of_request_by_admin) > print_request.no_of_print:
                    return Response({'status': False, 'message': f'No of request by admin cannot exceed {print_request.no_of_print}'})
            
            # Create PrintRequestApproval object
            print_request_approval = PrintRequestApproval.objects.create(
                user=user,
                print_request=print_request,
                no_of_request_by_admin=no_of_request_by_admin if status == 'approved' else None,
                status=status
            )
            
            return Response({'status': True, 'message': f'Print request {status} successfully', 'data': {'approval_id': print_request_approval.id}})
        
        except Exception as e:
            return Response({'status': False, 'message': 'Something went wrong', 'error': str(e)})
        

class PrintRequestUpdateAPI(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            # Get request data
            print_request_id = self.kwargs.get('print_request_id')
            status = request.data.get('status')

            # Validate that the print_request_id is provided
            if not print_request_id:
                return Response({'status': False, 'message': 'Print request ID is required'})

            # Fetch the associated PrintRequest object
            try:
                print_request = PrintRequest.objects.get(id=print_request_id)
            except PrintRequest.DoesNotExist:
                return Response({'status': False, 'message': 'Invalid Print Request ID'})

            # Fetch the PrintRequestApproval for the associated PrintRequest
            try:
                print_request_approval = PrintRequestApproval.objects.get(print_request=print_request, status='approved')
            except PrintRequestApproval.DoesNotExist:
                return Response({'status': False, 'message': 'No approved PrintRequestApproval found for this PrintRequest'})

            # Check if the status of the PrintRequest is 'print_is_pending'
            if print_request.status != 'print_is_pending':
                return Response({'status': False, 'message': 'This PrintRequest is not in a pending state'})

            # Update the no_of_print and status fields in PrintRequest
            print_request.status = status
            print_request.save()

            return Response({'status': True, 'message': 'Data Printing started successfully'})
        
        except Exception as e:
            return Response({'status': False, 'message': 'Something went wrong', 'error': str(e)})

