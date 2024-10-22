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


class WorkFlowUpdateSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WorkFlowSerializer
    lookup_field = 'workflow_id'

    def update(self, request, *args, **kwargs):
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
    # permission_classes = [permissions.IsAuthenticated]
    
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
        
        
class PrintRequestViewSet(viewsets.ModelViewSet):
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
        

class PrintApprovalViewSet(viewsets.ModelViewSet):
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
        

class PrintRequestUpdateViewSet(viewsets.ModelViewSet):
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


class DocumentCreateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()
    
    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            document_title = request.data.get('document_title')
            document_number = request.data.get('document_number')
            document_type = request.data.get('document_type')
            document_description = request.data.get('document_description', '')
            revision_time = request.data.get('revision_time', '')
            document_operation = request.data.get('document_operation', '')
            select_template = request.data.get('select_template')
            workflow = request.data.get('workflow')
            
            # Validation for required fields
            if not document_title:
                return Response({"status": False, "message": "Document title is required", "data": []})
            if not document_type:
                return Response({"status": False, "message": "Document type is required", "data": []})
            if not workflow:
                return Response({"status": False, "message": "Workflow is required", "data": []})

            # Handle operation-specific validations
            if document_operation == 'create_online':
                if not select_template:
                    return Response({"status": False, "message": "Template selection is required for creating document online", "data": []})
            
            # Create a new Document object
            document = Document.objects.create(
                user=user,
                document_title=document_title,
                document_number=document_number,
                document_type_id=document_type,
                document_description=document_description,
                revision_time=revision_time,
                document_operation=document_operation,
                select_template_id=select_template if document_operation == 'create_online' else None,
                workflow_id=workflow
            )

            # If the operation is 'upload_file', handle the Word file upload
            # if document_operation == 'upload_file':
            #     word_file = request.FILES['word_file']
            #     UploadedDocument.objects.create(
            #         document=document,
            #         word_file=word_file
            #     )
            
            # Serialize the created document
            serializer = DocumentSerializer(document)
            return Response({"status": True, "message": "Document created successfully", "data": serializer.data})
        
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})


class DocumentUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()
    lookup_field = 'document_id'

    def update(self, request, *args, **kwargs):
        try:
            document_id = self.kwargs.get('document_id')
            
            try:
                document = Document.objects.get(id=document_id)
            except Document.DoesNotExist:
                return Response({'status': False, 'message': 'Document not found'})

            # Extract fields from the request data
            document_title = request.data.get('document_title')
            document_number = request.data.get('document_number')
            document_type = request.data.get('document_type')
            document_description = request.data.get('document_description')
            revision_time = request.data.get('revision_time')
            document_operation = request.data.get('document_operation')
            # select_template = request.data.get('select_template')
            workflow = request.data.get('workflow')

      
            if document_operation == 'upload_file':
                word_file = request.FILES['word_file']
                UploadedDocument.objects.create(
                    document=document,
                    word_file=word_file
                )

            # Update the document fields
            if document_title != '':
                document.document_title = document_title
            if document_number != '':
                document.document_number = document_number
            if document_type != '':
                document.document_type = document_type
            if document_description != '':
                document.document_description = document_description
            if revision_time != '':
                document.revision_time = revision_time
            if document_operation != '':
                document.document_operation = document_operation
            if workflow != '':
                document.workflow = workflow

            # Save the updated document
            document.save()

            # Serialize the updated document
            serializer = DocumentSerializer(document)
            return Response({"status": True, "message": "Document updated successfully", "data": serializer.data})
        
        except Exception as e:
            return Response({"status": False, "message": 'Something went wrong', 'error': str(e)})
        

class DocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentSerializer
    queryset = Document.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['document_title', 'document_number', 'document_description', 'document_type__name']
    ordering_fields = ['document_title', 'created_at'] 

    def list(self, request):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            if queryset.exists():
                serializer = DocumentSerializer(queryset, many=True)
                return Response({
                    "status": True,
                    "message": "Documents fetched successfully",
                    'total': queryset.count(),
                    'data': serializer.data
                })
            else:
                return Response({
                    "status": True,
                    "message": "No Documents found",
                    "total": 0,
                    "data": []
                })
        except Exception as e:
            return Response({"status": False, 'message': 'Something went wrong', 'error': str(e)})
        
class DocumentDeleteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            document_id = request.data.get('document_id')

            if not Document.objects.filter(id=document_id).exists():
                return Response({"status": False, "message": "Document ID not found"})

            # Retrieve and delete the document
            document_object = Document.objects.get(id=document_id)
            document_object.delete()

            return Response({"status": True, "message": "Document deleted successfully"})

        except Exception as e:
            return Response({"status": False, 'message': 'Something went wrong', 'error': str(e)})
        


class TemplateCreateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = TemplateModel.objects.all()
    
    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            template_name = request.data.get('template_name')
            template_doc = request.FILES.get('template_doc')  # Get the uploaded file
            
            if not template_name:
                return Response({"status": False, "message": "Template name is required", "data": []})
            if not template_doc:
                return Response({"status": False, "message": "Template document is required", "data": []})
            
            template = TemplateModel.objects.create(
                template_name=template_name,
                user=user, 
                template_doc=template_doc
            )
            
            return Response({"status": True, "message": "Template created successfully"})
        
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        


class TemplateUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = TemplateModel.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        try:
            template_id = self.kwargs.get('id') 

            try:
                template = TemplateModel.objects.get(id=template_id)
            except TemplateModel.DoesNotExist:
                return Response({'status': False, 'message': 'Template not found'})

            template_name = request.data.get('template_name')
            template_doc = request.FILES.get('template_doc') 

            if template_name is not None:
                template.template_name = template_name
            if template_doc is not None:
                template.template_doc = template_doc  

            template.save()

            return Response({"status": True, "message": "Template updated successfully"})
        
        except Exception as e:
            return Response({"status": False, "message": 'Something went wrong', 'error': str(e)})
        
class DynamicStatusCreateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DynamicStatus.objects.all()
    serializer_class = DynamicStatusSerializer

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            status_name = request.data.get('status_name')
            status_value = request.data.get('status')

            if not status_name:
                return Response({"status": False, "message": "Status name is required"}, status=status.HTTP_400_BAD_REQUEST)
            if not status_value:
                return Response({"status": False, "message": "Status is required"}, status=status.HTTP_400_BAD_REQUEST)

            dynamic_status = DynamicStatus.objects.create(
                user=user,
                status_name=status_name,
                status=status_value
            )

            serializer = DynamicStatusSerializer(dynamic_status)
            return Response({"status": True, "message": "Dynamic status created successfully", "data": serializer.data})

        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})

class DynamicStatusListViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DynamicStatus.objects.all()
    serializer_class = DynamicStatusSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": True, "message": "Dynamic statuses fetched successfully", "data": serializer.data})

class DynamicStatusUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DynamicStatusSerializer
    queryset = DynamicStatus.objects.all()
    lookup_field = 'id'  # Assuming you want to look up by primary key

    def update(self, request, *args, **kwargs):
        try:
            dynamic_status_id = self.kwargs.get('id')
            dynamic_status = self.get_object()

            status_name = request.data.get('status_name')
            status_value = request.data.get('status')

            if status_name is not None:
                dynamic_status.status_name = status_name
            if status_value is not None:
                dynamic_status.status = status_value
            
            dynamic_status.save()
            serializer = DynamicStatusSerializer(dynamic_status)
            return Response({"status": True, "message": "Dynamic status updated successfully", "data": serializer.data})

        except DynamicStatus.DoesNotExist:
            return Response({"status": False, "message": "Dynamic status not found"})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})

class DynamicStatusDeleteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DynamicStatus.objects.all()
    serializer_class = DynamicStatusSerializer
    lookup_field = 'id'  # Assuming you want to look up by primary key

    def destroy(self, request, *args, **kwargs):
        try:
            dynamic_status = self.get_object()
            dynamic_status.delete()
            return Response({"status": True, "message": "Dynamic status deleted successfully"})

        except DynamicStatus.DoesNotExist:
            return Response({"status": False, "message": "Dynamic status not found"})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})

class DocumentDetailsCreateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DocumentDetails.objects.all()
    serializer_class = DocumentDetailsSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            document_id = request.data.get('document_id') 
            document_data = request.data.get('document_data') 

            # Check if the required fields are provided
            if not document_id:
                return Response({"status": False, "message": "Document ID is required", "data": []})
            if not document_data:
                return Response({"status": False, "message": "Document data is required", "data": []})

            # Fetch the document instance based on the provided document_id
            try:
                document = Document.objects.get(id=document_id)
            except Document.DoesNotExist:
                return Response({"status": False, "message": "Document not found", "data": []})

            # Create a new DocumentDetails entry
            document_details = DocumentDetails.objects.create(
                user=user,
                document=document, 
                document_data=document_data
            )
            
            return Response({"status": True, "message": "Document created successfully", "data": DocumentDetailsSerializer(document_details).data})
        
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})


class DocumentDetailsUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DocumentDetails.objects.all()
    lookup_field = 'docdetail_id'  
    serializer_class = DocumentDetailsSerializer

    def update(self, request, *args, **kwargs):
        try:
            documentdetail_id = self.kwargs.get('docdetail_id')

            try:
                document_details = DocumentDetails.objects.get(id=documentdetail_id)
            except DocumentDetails.DoesNotExist:
                return Response({"status": False, "message": "Document not found"})

            # Get new data from the request
            document_data = request.data.get('document_data')
            document_id = request.data.get('document_id') 


            if document_data is not None:
                document_details.document_data = document_data
            
            if document_id is not None:
                document_details.document_id = document_id

            document_details.save() 

            return Response({
                "status": True,
                "message": "Document Details updated successfully",
            })

        except Exception as e:
            return Response({
                "status": False,
                "message": "Something went wrong",
                "error": str(e)
            })
        

class DocumentDetailsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentDetailsSerializer
    queryset = DocumentDetails.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['document__name', 'user__username'] 
    ordering_fields = ['created_at']

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset()) 
        
        try:
            if queryset.exists():
                serializer = DocumentDetailsSerializer(queryset, many=True)
                return Response({
                    "status": True,
                    "message": "Documents fetched successfully",
                    'total': queryset.count(),
                    'data': serializer.data
                })
            else:
                return Response({
                    "status": True,
                    "message": "No Documents found",
                    "total": 0,
                    "data": []
                })
        except Exception as e:
            return Response({"status": False, 'message': 'Something went wrong', 'error': str(e)})


