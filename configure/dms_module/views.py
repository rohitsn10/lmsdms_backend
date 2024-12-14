from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.response import Response
from .models import *
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from rest_framework import permissions
from user_profile.function_call import *
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from user_profile.email_utils import *
from django.db.models import Q


class CustomPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'  # Allow users to set page size
    max_page_size = 100  # Maximum page size


class DashboardCountViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            document_count = Document.objects.count()
            workflow_count = WorkFlowModel.objects.count()
            document_type_count = DocumentType.objects.count()
            user_count = CustomUser.objects.count()
            department_count = Department.objects.count()

            return Response({
                "status": True,
                "message": "Dashboard counts fetched successfully",
                "data": {
                    "document_count": document_count,
                    "workflow_count": workflow_count,
                    "document_type_count": document_type_count,
                    "user_count" : user_count,
                    "department_count" : department_count
                }
            })
        except Exception as e:
            return Response({
                "status": False,
                "message": "Something went wrong",
                "error": str(e)
            })

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
                
class PrintRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = PrintRequest.objects.all().order_by('-id')

    def create(self, request):
        try:
            user = self.request.user
            sop_document_id = request.data.get('sop_document_id')
            no_of_print = request.data.get('no_of_print')
            issue_type = request.data.get('issue_type')
            reason_for_print = request.data.get('reason_for_print')
            printer_id = request.data.get('printer_id')


            if not no_of_print:
                return Response({'status': False, 'message': 'NO of print is required'})
            if not issue_type:
                return Response({'status': False, 'message': 'Issue type is required'})
            if not reason_for_print:
                return Response({'status': False, 'message': 'Reason is required'})
            if not printer_id:
                return Response({'status': False, 'message': 'Printer id is required'})
            
            try:
                sop_document = Document.objects.get(id=sop_document_id)
            except Document.DoesNotExist:
                return Response({'status': False, 'message': 'Invalid document id'})
            
            try:
                printer = PrinterMachinesModel.objects.get(id=printer_id)
            except Document.DoesNotExist:
                return Response({'status': False, 'message': 'Invalid printer id'})

            printrequest_obj = PrintRequest.objects.create(
                user = user,
                no_of_print=no_of_print,
                issue_type=issue_type,
                reason_for_print=reason_for_print,
                sop_document_id = sop_document,
                printer = printer,
            )
            user_department = user.department
            qa_group = Group.objects.get(name='Reviewer')
            qa_users_in_department = CustomUser.objects.filter(groups=qa_group, department=user_department)
            send_print_request_email(user, no_of_print, reason_for_print, sop_document, issue_type, qa_users_in_department)
            return Response({'status': True, 'message': 'Print requested successfully'})
        except Exception as e:
            return Response({'status': False, 'message': 'Something went wrong', 'error': str(e)})
        
    def list(self, request, *args, **kwargs):
        try:
            queryset = PrintRequest.objects.all()
            serializer = PrintRequestSerializer(queryset, many=True)
            return Response({"status": True, "message": "Print request list fetched successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

# class PrintApprovalViewSet(viewsets.ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = PrintRequestApproval.objects.all().order_by('-id')

#     def create(self, request, *args, **kwargs):
#         try:
#             user = self.request.user
#             print_request_id = request.data.get('print_request_id')
#             no_of_request_by_admin = request.data.get('no_of_request_by_admin')
#             status = request.data.get('status')

#             # Validate that the print_request_id is provided
#             if not print_request_id:
#                 return Response({'status': False, 'message': 'Print request ID is required'})
            
#             # Fetch the associated PrintRequest object
#             try:
#                 print_request = PrintRequest.objects.get(id=print_request_id)
#             except PrintRequest.DoesNotExist:
#                 return Response({'status': False, 'message': 'Invalid Print Request ID'})
            
#             if not no_of_request_by_admin:
#                 return Response({'status': False, 'message': 'No of request by admin is required when approving'})
            
#             # Ensure no_of_request_by_admin does not exceed no_of_print from PrintRequest
#             if int(no_of_request_by_admin) > print_request.no_of_print:
#                 return Response({'status': False, 'message': f'No of request by admin cannot exceed {print_request.no_of_print}'})
            
#             # Fetch the DynamicStatus object for the provided status
#             try:
#                 dynamic_status = DynamicStatus.objects.get(id=status)
#             except DynamicStatus.DoesNotExist:
#                 return Response({'status': False, 'message': 'Invalid status value provided'})
            
#             # Generate the unique approval number
#             base_format = "BPL-Dms-"

#             # Track the last approval for the current print_request
#             last_approval = PrintRequestApproval.objects.filter(print_request=print_request).order_by('-id').first()

#             # Initialize the copy number for the first approval
#             if last_approval:
#                 # Extract the last copy number and increment it
#                 last_copy_number = int(last_approval.approval_number.split('-')[-2])
#                 new_copy_number = last_copy_number + 1
#             else:
#                 # If no approval exists yet, start from 01
#                 new_copy_number = 1

#             # Ensure that the generated approval number is unique
#             approval_number = f"{base_format}{str(new_copy_number).zfill(2)}-{no_of_request_by_admin}"

#             # Check if the generated approval number already exists, and keep incrementing until it's unique
#             while PrintRequestApproval.objects.filter(approval_number=approval_number).exists():
#                 new_copy_number += 1
#                 approval_number = f"{base_format}{str(new_copy_number).zfill(2)}-{no_of_request_by_admin}"

#             # Create PrintRequestApproval object
#             print_request_approval = PrintRequestApproval.objects.create(
#                 user=user,
#                 print_request=print_request,
#                 no_of_request_by_admin=no_of_request_by_admin,
#                 status=dynamic_status,
#                 approval_number=approval_number
#             )
            
#             return Response({'status': True, 'message': f'Print request successfully'})
        
#         except Exception as e:
#             return Response({'status': False, 'message': 'Something went wrong', 'error': str(e)})

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
            
            if not no_of_request_by_admin:
                return Response({'status': False, 'message': 'No of request by admin is required when approving'})
            
            # Ensure no_of_request_by_admin does not exceed no_of_print from PrintRequest
            if int(no_of_request_by_admin) > print_request.no_of_print:
                return Response({'status': False, 'message': f'No of request by admin cannot exceed {print_request.no_of_print}'})
            
            # Fetch the DynamicStatus object for the provided status
            try:
                dynamic_status = DynamicStatus.objects.get(id=status)
            except DynamicStatus.DoesNotExist:
                return Response({'status': False, 'message': 'Invalid status value provided'})
            
            # Generate unique approval numbers
            base_format = "BPL-Dms-"
            approval_numbers = []
            for i in range(int(no_of_request_by_admin)):
                new_copy_number = 1  # Start from 1
                approval_number = f"{base_format}{str(new_copy_number).zfill(2)}-{i+1}"

                # Ensure uniqueness in the database
                while ApprovalNumber.objects.filter(number=approval_number).exists():
                    new_copy_number += 1
                    approval_number = f"{base_format}{str(new_copy_number).zfill(2)}-{i+1}"

                # Create or get the unique approval number
                approval_number_obj, _ = ApprovalNumber.objects.get_or_create(number=approval_number)
                approval_numbers.append(approval_number_obj)

            # Create PrintRequestApproval object
            print_request_approval = PrintRequestApproval.objects.create(
                user=user,
                print_request=print_request,
                no_of_request_by_admin=no_of_request_by_admin,
                status=dynamic_status,
            )

            # Add approval numbers to the ManyToManyField
            print_request_approval.approval_numbers.add(*approval_numbers)
            
            return Response({
                'status': True,
                'message': 'Print request successfully approved',
            })
        
        except Exception as e:
            return Response({'status': False, 'message': 'Something went wrong', 'error': str(e)})

        

class PrintRequestUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            print_request_id = self.kwargs.get('print_request_id')
            status = request.data.get('status')

            if not print_request_id:
                return Response({'status': False, 'message': 'Print request ID is required'})

            try:
                print_request = PrintRequest.objects.get(id=print_request_id)
            except PrintRequest.DoesNotExist:
                return Response({'status': False, 'message': 'Invalid Print Request ID'})

            try:
                print_request_approval = PrintRequestApproval.objects.get(print_request=print_request, status='approved')
            except PrintRequestApproval.DoesNotExist:
                return Response({'status': False, 'message': 'No approved PrintRequestApproval found for this PrintRequest'})

            if print_request.status != 'print_is_pending':
                return Response({'status': False, 'message': 'This PrintRequest is not in a pending state'})

            print_request.status = status
            print_request.save()

            return Response({'status': True, 'message': 'Data Printing started successfully'})
        
        except Exception as e:
            return Response({'status': False, 'message': 'Something went wrong', 'error': str(e)})


class DocumentCreateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentdataSerializer
    queryset = Document.objects.all()
    
    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            document_title = request.data.get('document_title')
            document_number = request.data.get('document_number')
            document_type = request.data.get('document_type')
            document_description = request.data.get('document_description', '')
            revision_date = request.data.get('revision_date', '')
            document_operation = request.data.get('document_operation', '')
            select_template = request.data.get('select_template')
            workflow = request.data.get('workflow')
            document_current_status_id = request.data.get('document_current_status_id')
            training_required = request.data.get('training_required')
            visible_to_users = request.data.get('visible_to_users', [])

             # Ensure visible_to_users is parsed into a proper list
            if isinstance(visible_to_users, str):
                import json
                try:
                    visible_to_users = json.loads(visible_to_users)
                except json.JSONDecodeError:
                    return Response({
                        "status": False,
                        "message": "Invalid format for visible_to_users. Provide a valid list of IDs.",
                        "data": []
                    })

            # Validation for required fields
            if not document_title:
                return Response({"status": False, "message": "Document title is required", "data": []})
            if not document_type:
                return Response({"status": False, "message": "Document type is required", "data": []})
            if not workflow:
                return Response({"status": False, "message": "Workflow is required", "data": []})
            if not select_template:
                    return Response({"status": False, "message": "Template selection is required", "data": []})

            if revision_date:
                try:
                    revision_date = datetime.strptime(revision_date, "%Y-%m-%d").date()
                except ValueError:
                    return Response({
                        "status": False,
                        "message": "Invalid revision_date format. Use 'YYYY-MM-DD'.",
                        "data": []
                    })

            # Fetch the default status
            try:
                default_status = DynamicStatus.objects.get(id=document_current_status_id)  # Assuming status with ID 1 is the default
            except DynamicStatus.DoesNotExist:
                return Response({"status": False, "message": "Default status not found in the system", "data": []})

            # Create a new Document object
            document = Document.objects.create(
                user=user,
                document_title=document_title,
                document_number=document_number,
                document_type_id=document_type,
                document_description=document_description,
                revision_date=revision_date,
                document_operation=document_operation,
                select_template_id=select_template,
                workflow_id=workflow,
                document_current_status=default_status,
                version="1.0",
                training_required=training_required,

            )
            if visible_to_users:
                document.visible_to_users.set(visible_to_users)

            document.save()
            DocumentVersion.objects.create(
                document=document,
                version_number=document.version,
                updated_by=user,
            )

            # reviewer_group = Group.objects.get(name='Reviewer')
            # reviewers = CustomUser.objects.filter(groups=reviewer_group)
            # department_users = CustomUser.objects.filter(department=user.department)
            # users_to_notify = reviewers.union(department_users).distinct()
            # send_document_create_email(user, document_title, users_to_notify)

            # If the operation is 'upload_file', handle the Word file upload
            # if document_operation == 'upload_file':
            #     word_file = request.FILES['word_file']
            #     UploadedDocument.objects.create(
            #         document=document,
            #         word_file=word_file
            #     )
            
            # Serialize the created document
            # serializer = DocumentdataSerializer(document)
            return Response({"status": True, "message": "Document created successfully"})
        
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})


class DocumentUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()
    lookup_field = 'document_id'

    def update(self, request, *args, **kwargs):
        try:
            user = self.request.user
            document_id = self.kwargs.get('document_id')
            
            try:
                document = Document.objects.get(id=document_id)
            except Document.DoesNotExist:
                return Response({'status': False, 'message': 'Document not found'})

            # Extract fields from the request data
            document_title = request.data.get('document_title')
            document_number = request.data.get('document_number')
            document_type_id = request.data.get('document_type')
            document_description = request.data.get('document_description')
            revision_time = request.data.get('revision_time')
            document_operation = request.data.get('document_operation')
            workflow_id = request.data.get('workflow')

            if not document_title:
                return Response({"status": False, "message": "Document title is required", "data": []})
            if not document_type_id:
                return Response({"status": False, "message": "Document type is required", "data": []})
            if not workflow_id:
                return Response({"status": False, "message": "Workflow is required", "data": []})

            try:
                document_type = DocumentType.objects.get(id=document_type_id)
            except DocumentType.DoesNotExist:
                return Response({'status': False, 'message': 'Document type not found'})
            
            try:
                workflow = WorkFlowModel.objects.get(id=workflow_id)
            except WorkFlowModel.DoesNotExist:
                return Response({'status': False, 'message': 'Workflow not found'}, status=400)


      
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

            return Response({"status": True, "message": "Document updated successfully"})
        
        except Exception as e:
            return Response({"status": False, "message": 'Something went wrong', 'error': str(e)})
        

# class DocumentViewSet(viewsets.ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = DocumentviewSerializer
#     queryset = Document.objects.all().order_by('-id')
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ['document_title', 'document_number', 'document_description', 'document_type__name']
#     ordering_fields = ['document_title', 'created_at'] 

#     def list(self, request):
#         try:
#             queryset = self.filter_queryset(self.get_queryset())

#             if queryset.exists():
#                 serializer = DocumentviewSerializer(queryset, many=True)
#                 return Response({
#                     "status": True,
#                     "message": "Documents fetched successfully",
#                     'total': queryset.count(),
#                     'data': serializer.data
#                 })
#             else:
#                 return Response({
#                     "status": True,
#                     "message": "No Documents found",
#                     "total": 0,
#                     "data": []
#                 })
#         except Exception as e:
#             return Response({"status": False, 'message': 'Something went wrong', 'error': str(e)})

class DocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentviewSerializer
    queryset = Document.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['document_title', 'document_number', 'document_description', 'document_type__name']
    ordering_fields = ['document_title', 'created_at'] 

    def list(self, request):
        try:
            user = request.user 

             # Get the user's group IDs
            user_group_ids = user.groups.values_list('id', flat=True)

            # Initialize the queryset
            if user.groups.filter(name='Admin').exists():
                # Admins can see all documents
                queryset = Document.objects.all().order_by('-id')
            elif user.groups.filter(name='Reviewer').exists():
                # Reviewers can only see documents where they are in visible_to_users
                queryset = Document.objects.filter(visible_to_users=user).order_by('-id')
            elif user.department:
                # Non-reviewer users with a department can see documents created by users in their department
                queryset = Document.objects.filter(user__department=user.department).order_by('-id')
            else:
                queryset = Document.objects.none()

            # Apply search and ordering filters
            queryset = self.filter_queryset(queryset)

            # Serialize and respond
            if queryset.exists():
                serializer = self.serializer_class(queryset, many=True)
                return Response({
                    "status": True,
                    "message": "Documents fetched successfully",
                    'total': queryset.count(),
                    'user_group_ids': list(user_group_ids) ,
                    'data': serializer.data,
                })
            else:
                return Response({
                    "status": True,
                    "message": "No Documents found",
                    "total": 0,
                    'user_group_ids': list(user_group_ids),  
                    "data": [],

                })
        except Exception as e:
            return Response({
                "status": False,
                'message': 'Something went wrong',
                'error': str(e)
            })
        
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
        

class DocumentTemplateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentdataSerializer
    queryset = Document.objects.all()
    lookup_field = 'document_id'

    def list(self, request, *args, **kwargs):
        document_id = self.kwargs.get('document_id')

        if document_id is None:
            return Response({"status": False, "message": "document_id parameter is required"})

        try:
            document = Document.objects.get(id=document_id)
            serializer = self.get_serializer(document, context={'request': request})
            return Response({
                "status": True,
                "message": "Template data fetched successfully",
                "data": serializer.data
            })

        except Document.DoesNotExist:
            return Response({"status": False, "message": "Document not found"})



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
        
class TemplateViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TemplateSerializer
    queryset = TemplateModel.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['template_name', 'user__username']
    ordering_fields = ['template_name', 'created_at']

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            if queryset.exists():
                serializer = self.get_serializer(queryset, many=True)
                return Response({
                    "status": True,
                    "message": "Templates fetched successfully",
                    'total': queryset.count(),
                    'data': serializer.data
                })
            else:
                return Response({
                    "status": True,
                    "message": "No templates found",
                    "total": 0,
                    "data": []
                })
        except Exception as e:
            return Response({
                "status": False,
                'message': 'Something went wrong',
                'error': str(e)
            })

class TemplateUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = TemplateModel.objects.all()
    lookup_field = 'temp_id'

    def update(self, request, *args, **kwargs):
        try:
            template_id = self.kwargs.get('temp_id') 

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
        

class TemplateDocumentViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'template_id'


    def list(self, request, *args, **kwargs):
        template_id = self.kwargs.get('template_id')

        if not template_id:
            return Response({"status": False, "message": "template_id parameter is required"})

        try:
            template = TemplateModel.objects.get(id=template_id)
            serializer = TemplateDocumentSerializer(template, context={'request': request})
            return Response({
                "status": True,
                "message": "Template document fetched successfully",
                "data": serializer.data
            })
        except TemplateModel.DoesNotExist:
            return Response({"status": False, "message": "Template not found"})


        
class DynamicStatusCreateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DynamicStatus.objects.all()
    serializer_class = DynamicStatusSerializer

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            status_value = request.data.get('status')

          
            if not status_value:
                return Response({"status": False, "message": "Status is required"})

            dynamic_status = DynamicStatus.objects.create(
                user=user,
                status=status_value
            )

            return Response({"status": True, "message": "Dynamic status created successfully"})

        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})
        

class DynamicStatusListViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DynamicStatus.objects.all().order_by('-id')
    serializer_class = DynamicStatusSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['status', 'user__username']
    ordering_fields = ['status', 'created_at']

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            if queryset.exists():
                serializer = self.get_serializer(queryset, many=True)
                return Response({
                    "status": True,
                    "message": "Dynamic statuses fetched successfully",
                    'total': queryset.count(),
                    'data': serializer.data
                })
            else:
                return Response({
                    "status": True,
                    "message": "No dynamic statuses found",
                    "total": 0,
                    "data": []
                })
        except Exception as e:
            return Response({
                "status": False, 
                'message': 'Something went wrong', 
                'error': str(e)
            })
        

class DynamicStatusUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DynamicStatusSerializer
    queryset = DynamicStatus.objects.all()
    lookup_field = 'dynamic_status_id'  

    def update(self, request, *args, **kwargs):
        try:
            dynamic_status_id = self.kwargs.get('dynamic_status_id')
            dynamic_status = DynamicStatus.objects.get(id=dynamic_status_id)

            status_value = request.data.get('status')

          
            if status_value is not None:
                dynamic_status.status = status_value
            
            dynamic_status.save()
            return Response({"status": True, "message": "Dynamic status updated successfully"})

        except DynamicStatus.DoesNotExist:
            return Response({"status": False, "message": "Dynamic status not found"})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})

# class DynamicStatusDeleteViewSet(viewsets.ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = DynamicStatus.objects.all()
#     serializer_class = DynamicStatusSerializer
#     lookup_field = 'dynamic_status_id'  

#     def destroy(self, request, *args, **kwargs):
#         try:
#             dynamic_status_id = self.kwargs.get('dynamic_status_id')
#             dynamic_status = DynamicStatus.objects.get(id=dynamic_status_id)      
#             dynamic_status.delete()
#             return Response({"status": True, "message": "Dynamic status deleted successfully"})

#         except DynamicStatus.DoesNotExist:
#             return Response({"status": False, "message": "Dynamic status not found"})
#         except Exception as e:
#             return Response({"status": False, "message": "Something went wrong", "error": str(e)})

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
            
            return Response({"status": True, "message": "Document created successfully"})
        
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
            
            # if document_id is not None:
            #     document_details.document_id = document_id
            version_number = document_details.document.version  # Get the current version
            new_version = increment_version(version_number)
            document_details.document.version = new_version
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


class DocumentApproveActionCreateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DocumentAuthorApproveAction.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            document = request.data.get('document_id')
            # document_id = request.data.get('documentdetails_id')
            status_id = request.data.get('status')

            # Ensure required fields are provided
            # if not document_id:
            #     return Response({"status": False, "message": "Document details are required"})
            if not document:
                return Response({"status": False, "message": "Document are required"})
            if not status_id:
                return Response({"status": False, "message": "Status is required"})

            # Fetch related document and status objects
            document = Document.objects.get(id=document)
            # documentdetails = DocumentDetails.objects.get(id=document_id)
            status = DynamicStatus.objects.get(id=status_id)

            document_approve_action = DocumentAuthorApproveAction.objects.create(
                user=user,
                document=document,
                # documentdetails_approve=documentdetails,
                status_approve=status
            )
            approve_action = DocApprove.objects.create(
                user=user,
                document=document,
                status_approve=status
            )
            document.document_current_status = status
            document.form_status = None
            document.assigned_to = None
            document.save()
            
            # document_title = document.document_title
            # reviewer_group = Group.objects.get(name='Reviewer')
            # reviewers = CustomUser.objects.filter(groups=reviewer_group)
            # department_users = CustomUser.objects.filter(department=user.department)
            # users_to_notify = reviewers.union(department_users).distinct()
            # send_document_update_email(user, document_title, users_to_notify)
            
           

            return Response({"status": True, "message": "Document approval action created successfully"})

        except DocumentDetails.DoesNotExist:
            return Response({"status": False, "message": "Invalid document details ID"})
        except DynamicStatus.DoesNotExist:
            return Response({"status": False, "message": "Invalid status ID"})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})


class DocumentReviewerActionCreateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DocumentReviewerAction.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            document_id = request.data.get('document_id')
            status_id = request.data.get('status')

            # Validate required fields
            if not document_id:
                return Response({"status": False, "message": "Document is required"})
            if not status_id:
                return Response({"status": False, "message": "Status is required"})

            # Fetch the document
            try:
                document = Document.objects.get(id=document_id)
            except Document.DoesNotExist:
                return Response({"status": False, "message": "Invalid Document ID"})

            # Fetch the status
            try:
                status = DynamicStatus.objects.get(id=status_id)
            except DynamicStatus.DoesNotExist:
                return Response({"status": False, "message": "Invalid Status ID"})

            # Check if the user is a reviewer for the document creator's department
            # user_department = document.user.department  # Assuming a department field in the user model
            # reviewers_in_department = CustomUser.objects.filter(
            #     department=user_department,
            #     groups__name="Reviewer"
            # )

            # Ensure the requesting user is among the reviewers
            # if user not in reviewers_in_department:
            #     return Response({"status": False, "message": "You are not authorized to review this document"})

            # Create the reviewer action
            document_reviewer_action = DocumentReviewerAction.objects.create(
                user=user,
                document=document,
                status_approve=status
            )
            approve_action = DocApprove.objects.create(
                user=user,
                document=document,
                status_approve=status
            )

            # Check if all reviewers in the department have approved the document
            # approved_reviewers = DocumentReviewerAction.objects.filter(
            #     document=document,
            #     status_approve=status
            # ).values_list('user', flat=True)

            # all_reviewers_approved = all(reviewer.id in approved_reviewers for reviewer in reviewers_in_department)

            # Update document current status only if all reviewers have approved
            # if all_reviewers_approved:
            document.document_current_status = status
            document.assigned_to = None
            document.save()
            document_title  = document.document_title
            approver_user = Group.objects.get(name='Approver')
            approvers = CustomUser.objects.filter(groups=approver_user)
            department_users = CustomUser.objects.filter(department=user.department)
            users_to_notify = approvers.union(department_users).distinct()
            send_document_approval_email(user, document_title, users_to_notify)

            return Response({
                "status": True,
                "message": "Document reviewer action created successfully",
            })

        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})


class DocumentApproverActionCreateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DocumentApproverAction.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            document_id = request.data.get('document_id')
            status_id = request.data.get('status')

            # Validate required fields
            if not document_id:
                return Response({"status": False, "message": "Document is required"})
            if not status_id:
                return Response({"status": False, "message": "Status is required"})

            # Fetch the document
            try:
                document = Document.objects.get(id=document_id)
            except Document.DoesNotExist:
                return Response({"status": False, "message": "Invalid Document ID"})

            # Fetch the status
            try:
                status = DynamicStatus.objects.get(id=status_id)
            except DynamicStatus.DoesNotExist:
                return Response({"status": False, "message": "Invalid Status ID"})

           
            # Create the reviewer action
            document_approver_action = DocumentApproverAction.objects.create(
                user=user,
                document=document,
                status_approve=status
            )
            approve_action = DocApprove.objects.create(
                user=user,
                document=document,
                status_approve=status
            )


            # Update document current status only if all reviewers have approved
            # if all_reviewers_approved:
            document.document_current_status = status
            document.assigned_to = None
            document.save()

            return Response({
                "status": True,
                "message": "Document approver action created successfully",
            })

        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})


class DocumentDocAdminActionCreateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DocumentDocAdminAction.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            document_id = request.data.get('document_id')
            status_id = request.data.get('status')

            # Validate required fields
            if not document_id:
                return Response({"status": False, "message": "Document is required"})
            if not status_id:
                return Response({"status": False, "message": "Status is required"})

            # Fetch the document
            try:
                document = Document.objects.get(id=document_id)
            except Document.DoesNotExist:
                return Response({"status": False, "message": "Invalid Document ID"})

            # Fetch the status
            try:
                status = DynamicStatus.objects.get(id=status_id)
            except DynamicStatus.DoesNotExist:
                return Response({"status": False, "message": "Invalid Status ID"})

           
            # Create the reviewer action
            document_docAdmin_action = DocumentDocAdminAction.objects.create(
                user=user,
                document=document,
                status_approve=status
            )

            approve_action = DocApprove.objects.create(
                user=user,
                document=document,
                status_approve=status
            )

            document.document_current_status = status
            document.save()

            # Log actions based on status
            if status_id == 7:  
                DocumentEffectiveAction.objects.create(
                    user=user,
                    documentdetails_effective=document,
                    status_effective=status
                )
            elif status_id == 6:  
                DocumentReleaseAction.objects.create(
                    user=user,
                    documentdetails_release=document,
                    status_release=status
                )

            return Response({
                "status": True,
                "message": "Document Doc Admin action created successfully",
            })

        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})


class DocumentSendBackActionCreateViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            document_id = request.data.get('document_id')
            assigned_to_id = request.data.get('assigned_to')
            status_id = request.data.get('status_sendback')
            group_id = request.data.get('assign_user_group')


            # Validate required fields
            if not document_id or not assigned_to_id or not status_id:
                return Response({
                    "status": False,
                    "message": "Document ID, Assigned User ID, and Status ID are required"
                })

            # Fetch the document
            try:
                document = Document.objects.get(id=document_id)
            except Document.DoesNotExist:
                return Response({"status": False, "message": "Invalid Document ID"})

            # Fetch the assigned user
            try:
                assigned_to = CustomUser.objects.get(id=assigned_to_id)
            except CustomUser.DoesNotExist:
                return Response({"status": False, "message": "Invalid Assigned User ID"})

            # Fetch the status
            try:
                status = DynamicStatus.objects.get(id=status_id)
            except DynamicStatus.DoesNotExist:
                return Response({"status": False, "message": "Invalid Status ID"})

            # Log the send-back action
            send_back_action = DocumentSendBackAction.objects.create(
                user=user,
                document=document,
                status_sendback=status,
                group = group_id
            )

            # Update the document's assigned user and reason
            document.assigned_to = assigned_to
            document.assigned_to_group = group_id
            document.document_current_status = status
            document.save()
            document_title = document.document_title
            send_document_sendback_email(assigned_to, document_title)
            
            return Response({
                "status": True,
                "message": "Document sent back successfully",
            })

        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})


class DocumentStatusHandleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DocumentReleaseAction.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            document_id = request.data.get('document_id')
            status_id = request.data.get('status_id')

            if not document_id:
                return Response({"status": False, "message": "Document details are required"})
            # if not status_id:
            #     return Response({"status": False, "message": "Status is required"})
            try:
                status_id = int(status_id)
            except (TypeError, ValueError):
                return Response({"status": False, "message": f"Invalid status ID: {status_id}"})

            status_release = DynamicStatus.objects.get(id=status_id)

            try:
                document = Document.objects.get(id=document_id)
            except Document.DoesNotExist:
                return Response({"status": False, "message": "Invalid Document ID"})
            
            current_date = now().date()
            
            # Determine which model to use based on status_id
            if status_id == 6:
                document_release_action = DocumentReleaseAction.objects.create(
                    user=user,
                    document_id=document_id,
                    status_release=status_release
                )
                document.document_current_status = status_release
                document.save()
                return Response({"status": True, "message": "Document release action created successfully"})
            elif status_id == 7:
                document_effective_action = DocumentEffectiveAction.objects.create(
                    user=user,
                    document_id=document_id,
                    status_effective=status_release
                )
                # Update the document's current status
                document.effective_date = current_date
                document.document_current_status = status_release
                document.save()
                return Response({"status": True, "message": "Document effective action created successfully"})
            else:
                return Response({"status": False, "message": "Invalid status ID"})            

        except Document.DoesNotExist:
            return Response({"status": False, "message": "Invalid document ID"})
        except DynamicStatus.DoesNotExist:
            return Response({"status": False, "message": "Invalid status ID"})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})


# class DocumentEffectiveActionCreateViewSet(viewsets.ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = DocumentEffectiveAction.objects.all()

#     def create(self, request, *args, **kwargs):
#         try:
#             user = self.request.user
#             document_id = request.data.get('documentdetails_effective')
#             status_id = request.data.get('status_effective')

#             if not document_id:
#                 return Response({"status": False, "message": "Document details are required"})
#             if not status_id:
#                 return Response({"status": False, "message": "Status is required"})

#             documentdetails_effective = DocumentDetails.objects.get(id=document_id)
#             status_effective = DynamicStatus.objects.get(id=status_id)

#             document_effective_action = DocumentEffectiveAction.objects.create(
#                 user=user,
#                 documentdetails_effective=documentdetails_effective,
#                 status_effective=status_effective
#             )

#             return Response({"status": True, "message": "Document effective action created successfully"})

#         except DocumentDetails.DoesNotExist:
#             return Response({"status": False, "message": "Invalid document details ID"})
#         except DynamicStatus.DoesNotExist:
#             return Response({"status": False, "message": "Invalid status ID"})
#         except Exception as e:
#             return Response({"status": False, "message": "Something went wrong", "error": str(e)})
        
#     def list(self, request, *args, **kwargs):
#         try:
#             user = self.request.user

#             queryset = DocumentEffectiveAction.objects.filter(user=user)

#             if queryset.exists():
#                 serializer = DocumentEffectiveActionSerializer(queryset, many=True)
#                 data = serializer.data
#                 return Response({"status": True, "message": "Document effective actions fetched successfully", "data": data})
#             else:
#                 return Response({"status": False, "message": "No document effective actions found", "data": []})
#         except Exception as e:
#             return Response({"status": False, "message": "Something went wrong", "error": str(e)})


         
class DocumentReviseActionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DocumentRevisionAction.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            document_id = request.data.get('document_id',None)
            status_id = request.data.get('status_id',None)
            request_action_id = request.data.get('request_action_id',None)
            action_status = request.data.get('action_status',None)

            if not document_id:
                return Response({"status": False, "message": "Document ID is required"})
            if not status_id:
                return Response({"status": False, "message": "Status ID is required"})
            if not request_action_id:
                return Response({"status": False, "message": "Revision request ID is required"})
            if not action_status or action_status not in ['approved', 'rejected']:
                return Response({"status": False, "message": "Action status is required and must be 'approved' or 'rejected'"})
            
            document = Document.objects.get(id=document_id)
            status_revision = DynamicStatus.objects.get(id=status_id)
            revision_request = DocumentRevisionRequestAction.objects.get(id=request_action_id)
            revision_request.status = action_status
            revision_request.save()
            revise_action = DocumentRevisionAction.objects.create(
                user=user,
                document=document,
                status_revision=status_revision
            )
            revise_action.save()
            document.is_revised = True
            document.save()

                # return Response({
                #     "status": True,
                #     "message": "Revise action created successfully",
                # })
            message = "Revision request successfully " + ("approved" if action_status == "approved" else "rejected")
            return Response({
                "status": True,
                "message": message,
            })
            
                # all_users = CustomUser.objects.filter(department = documentdetails_revise.document.user.department)
                # for user in all_users:
                #     send_document_revise_email(user, documentdetails_revise, status_revise)

        except Document.DoesNotExist:
            return Response({"status": False, "message": "Invalid document ID"})
        except DynamicStatus.DoesNotExist:
            return Response({"status": False, "message": "Invalid status ID"})
        except DocumentRevisionRequestAction.DoesNotExist:
            return Response({"status": False, "message": "Invalid revision request ID"})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})


class MasterCopyUserDropdownViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('-id')
    serializer_class = SimpleUserSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = SimpleUserSerializer(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "User list fetched successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class OtherUserDropdownViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('-id')
    serializer_class = SimpleUserSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = SimpleUserSerializer(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "User list fetched successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})


class DynamicInventoryCreateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DynamicInventory.objects.all()
    serializer_class = DynamicInventorySerializer

    def create(self, request, *args, **kwargs):
        try:
            inventory_name = request.data.get('inventory_name')
            if not inventory_name:
                return Response({"status": False, "message": "Inventory name is required"})

            dynamic_inventory = DynamicInventory.objects.create(inventory_name=inventory_name)
            serializer = DynamicInventorySerializer(dynamic_inventory)
            return Response({"status": True, "message": "Dynamic inventory created successfully", "data": serializer.data})

        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})

class DynamicInventoryListViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DynamicInventory.objects.all().order_by('-id')
    serializer_class = DynamicInventorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['inventory_name']
    ordering_fields = ['inventory_name', 'created_at']

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                "status": True,
                "message": "Dynamic inventories fetched successfully",
                'total': queryset.count(),
                'data': serializer.data
            })

        except Exception as e:
            return Response({"status": False, 'message': 'Something went wrong', 'error': str(e)})

class DynamicInventoryUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DynamicInventorySerializer
    queryset = DynamicInventory.objects.all()
    lookup_field = 'inventory_id'

    def update(self, request, *args, **kwargs):
        try:
            # Retrieve the inventory_id from the URL
            inventory_id = self.kwargs.get('inventory_id')
            
            # Retrieve inventory_name from the request data
            inventory_name = request.data.get('inventory_name')
            if not inventory_name:
                raise ValidationError("The field 'inventory_name' is required and cannot be null.")

            # Retrieve the inventory instance and update
            dynamic_inventory = DynamicInventory.objects.get(id=inventory_id)
            dynamic_inventory.inventory_name = inventory_name
            dynamic_inventory.save()

            # Serialize and return the updated data
            serializer = DynamicInventorySerializer(dynamic_inventory)
            return Response({
                "status": True, 
                "message": "Dynamic inventory updated successfully", 
                "data": serializer.data
            })

        except DynamicInventory.DoesNotExist:
            return Response({
                "status": False, 
                "message": "Dynamic inventory not found"
            })

        except ValidationError as ve:
            return Response({
                "status": False, 
                "message": str(ve)
            })

        except Exception as e:
            return Response({
                "status": False, 
                "message": "Something went wrong", 
                "error": str(e)
            })

class DynamicInventoryDeleteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DynamicInventory.objects.all()
    serializer_class = DynamicInventorySerializer
    lookup_field = 'inventory_id'

    def destroy(self, request, *args, **kwargs):
        try:
            inventory_id = self.kwargs.get('inventory_id')
            dynamic_inventory = DynamicInventory.objects.get(id=inventory_id)
            dynamic_inventory.delete()
            return Response({"status": True, "message": "Dynamic inventory deleted successfully"})

        except DynamicInventory.DoesNotExist:
            return Response({"status": False, "message": "Dynamic inventory not found"})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})
        


class DocumentCommentCreateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DocumentComments.objects.all().order_by('-created_at')

    def create(self, request):
        try:
            document_id = request.data.get('document')
            comment_description = request.data.get('comment_description', {})
            
            # Ensure required fields are provided
            if not document_id:
                return Response({'status': False, 'message': 'Document ID is required'})
            if not comment_description:
                return Response({'status': False, 'message': 'Comment description is required'})

            # Create the comment
            comment_obj = DocumentComments.objects.create(
                user=self.request.user,
                document_id=document_id,
                Comment_description=comment_description
            )
            return Response({'status': True, 'message': 'Comment added successfully'})
        except Exception as e:
            return Response({'status': False, 'message': 'Something went wrong', 'error': str(e)})
        
class DocumentCommentsViewSet(viewsets.ModelViewSet):
    queryset = DocumentComments.objects.all().order_by('-created_at')
    serializer_class = DocumentCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'document_id'


    def list(self, request, *args, **kwargs):
        try:
            document_id = self.kwargs.get('document_id')
            queryset = self.filter_queryset(self.get_queryset())

            if document_id:
                queryset = queryset.filter(document_id=document_id)

            serializer = DocumentCommentSerializer(queryset, many=True)
            data = serializer.data
            return Response({"message": "Comment list fetched successfully", "data": data})
        except Exception as e:
            return Response({"message": str(e), "data": []})
        
class DocumentCommentDeleteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'comment_id'

    def destroy(self, request, *args, **kwargs):
        try:
            comment_id = self.kwargs.get('comment_id')
            document_comment = DocumentComments.objects.get(id=comment_id)
            document_comment.delete()
            return Response({"message": "Comment deleted successfully"})

        except DocumentComments.DoesNotExist:
            return Response({"message": "Comment not found"})
        except Exception as e:
            return Response({"message": "Something went wrong", "error": str(e)})
        

class DocumentDetailViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'document_id'
    
    def list(self, request, *args, **kwargs):
        document_id = self.kwargs.get('document_id')

        if not document_id:
            return Response({"status": False, "message": "document_id parameter is required"})

        try:
            document = Document.objects.get(id=document_id)
            serializer = DocumentDetailSerializer(document)
            return Response({
                "status": True,
                "message": "Document details fetched successfully",
                "data": serializer.data
            })
        except Document.DoesNotExist:
            return Response({"status": False, "message": "Document not found"})
        
class DocumentDraftStatusViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Document.objects.all()

    def update(self, request, *args, **kwargs):
        try:
            user = request.user
            document_id = request.data.get('document_id')
            status_id = request.data.get('status_id')

            # Ensure required fields are provided
            if not document_id:
                return Response({"status": False, "message": "Document ID is required"})
            if not status_id:
                return Response({"status": False, "message": "Status ID is required"})

            # Fetch related document and status objects
            try:
                document = Document.objects.get(id=document_id)
            except Document.DoesNotExist:
                return Response({"status": False, "message": "Invalid Document ID"})

            try:
                status = DynamicStatus.objects.get(id=status_id)
            except DynamicStatus.DoesNotExist:
                return Response({"status": False, "message": "Invalid Status ID"})

            # Update the fields in the Document table
            document.document_current_status = status
            document.form_status = "save_draft"
            document.save()

            return Response({"status": True, "message": "Document Drafted successfully"})

        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})

class DocumentTypeUpdateViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentTypeSerializer
    queryset = DocumentType.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'document_type_id'       

    def update(self, request, *args, **kwargs):
        try:
            # Get document_type_id and new document_name from the request
            document_type_id = self.kwargs.get('document_type_id')
            document_name = request.data.get('document_name')

            # Validate document_type_id and document_name
            if not document_type_id:
                return Response({"status": False, "message": "Document type ID is required", "data": []})
            if not document_name:
                return Response({"status": False, "message": "Document name is required", "data": []})

            # Fetch the DocumentType instance
            document_type = DocumentType.objects.filter(id=document_type_id).first()
            if not document_type:
                return Response({"status": False, "message": "Document type not found", "data": []})

            # Update the document_name
            document_type.document_name = document_name
            document_type.save()

            # Serialize the updated instance
            serializer = DocumentTypeSerializer(document_type)
            return Response({"status": True, "message": "Document type updated successfully"})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})


# class DepartmentUsersViewSet(viewsets.ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = CustomUserdataSerializer

#     def list(self, request, *args, **kwargs):
#         try:
#             # Get the document ID from the request
#             document_id = request.data.get('document_id', None)
#             if not document_id:
#                 return Response({
#                     "status": False,
#                     "message": "Document ID is required.",
#                     "data": []
#                 })

#             # Fetch the document and ensure it exists
#             try:
#                 document = Document.objects.get(id=document_id)
#             except Document.DoesNotExist:
#                 return Response({
#                     "status": False,
#                     "message": "Document not found.",
#                     "data": []
#                 })

#             # Fetch users associated with the document from the DocApprove model
#             approved_users = CustomUser.objects.filter(
#                 docapprove__document=document
#             ).distinct()

#             # Serialize the filtered users
#             serializer = self.serializer_class(approved_users, many=True, context={'request': request})
#             return Response({
#                 "status": True,
#                 "message": "Users fetched successfully.",
#                 "data": serializer.data,
#             })
#         except Exception as e:
#             return Response({
#                 "status": False,
#                 "message": str(e),
#                 "data": [],
#             })


class DepartmentUsersViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'document_id'

    def list(self, request, *args, **kwargs):
        try:
            # Get the document ID from the request
            document_id = self.kwargs.get('document_id')
            if not document_id:
                return Response({
                    "status": False,
                    "message": "Document ID is required.",
                    "data": []
                })

            # Fetch the users linked to the document ID in the DocApprove model
            approved_users = DocApprove.objects.filter(document_id=document_id).select_related('user')
            if not approved_users.exists():
                return Response({
                    "status": False,
                    "message": "No users found for the given document ID.",
                    "data": []
                })

            # Prepare data for response
            response_data = []
            for approval in approved_users:
                user = approval.user
                user_groups = user.groups.all()
                for group in user_groups:
                    response_data.append({
                        "id": user.id,
                        "first_name": f"{user.first_name}({group.name})",
                        "group_id": [group.id],
                    })

            # Return the response
            return Response({
                "status": True,
                "message": "Users fetched successfully.",
                "data": response_data,
            })
        except Exception as e:
            return Response({
                "status": False,
                "message": str(e),
                "data": [],
            })

class PrinterMachines(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            printer_name = request.data.get('printer_name')
            printer_description = request.data.get('printer_location')

            if not printer_description:
                return Response({'status':False,'message':'Print Location is required'})
            
            if not printer_name:
                return Response({'status':False,'message':'Print Name is required'})
            
            printer_obj = PrinterMachinesModel.objects.create(
                user = user,
                printer_name = printer_name,
                printer_description = printer_description
            )
            return Response({'status': True, 'message': 'Printer Added successfully'})
        except Exception as e:
            return Response({'status': False, 'message': 'Something went wrong', 'error': str(e)})
    
    def list(self, request):
        queryset = PrinterMachinesModel.objects.all().order_by('-id')
        
        try:
            if queryset.exists():
                serializer = PrinterSerializer(queryset, many=True)
                return Response({
                    "status": True,
                    "message": "Printer Machine fetched successfully",
                    'total': queryset.count(),
                    'data': serializer.data
                })
            else:
                return Response({
                    "status": True,
                    "message": "No Printers found",
                    "total": 0,
                    "data": []
                })
        except Exception as e:
            return Response({"status": False, 'message': 'Something went wrong', 'error': str(e)})


class PrinterMachinesUpdate(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'printer_id'

    def update(self, request, *args, **kwargs):
        try:
            printer_id = self.kwargs.get("printer_id")
            printer_name = request.data.get('printer_name')
            printer_description = request.data.get('printer_location')
    
            printer_obj = PrinterMachinesModel.objects.get(id=printer_id)
            if printer_name:
                printer_obj.printer_name = printer_name
            if printer_description:
                printer_obj.printer_description = printer_description
            printer_obj.save()
    
            return Response({'status': True, 'message': 'Print machine updated successfully'})
        except PrinterMachinesModel.DoesNotExist:
            return Response({'status': False, 'message': 'Print not found'})
        except Exception as e:
            return Response({'status': False, 'message': 'Something went wrong', 'error': str(e)})
        
    def destroy(self, request, *args, **kwargs):
        try:
            printer_id = request.data.get('printer_id')   

            if not PrinterMachinesModel.objects.get(id=printer_id):
                return Response({"status":False, "message":"Print machine id not found"})
                     
            printer_object = PrinterMachinesModel.objects.get(id=printer_id)
            printer_object.delete()
            return Response({"status":True, "message":"Printer deleted succesfully"})
        except Exception as e:
                return Response({"status": False,'message': 'Something went wrong','error': str(e)})


class DocumentReviseRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DocumentRevisionRequestAction.objects.all()


    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            document_id = request.data.get('document_id')
            revise_description = request.data.get('revise_description')

            if not document_id:
                return Response({"status": False, "message": "Document ID is required"})
            if not revise_description:
                return Response({"status": False, "message": "Revise description is required"})

            document = Document.objects.get(id=document_id)

            revise_request = DocumentRevisionRequestAction.objects.create(
                user=user,
                document=document,
                revise_description=revise_description
            )

            return Response({
                "status": True,
                "message": "Revise request created successfully",
                "data": {}
            })
        except Document.DoesNotExist:
            return Response({"status": False, "message": "Invalid document ID"})
        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})


class DocumentReviseRequestGetViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentSerializer

    def get_queryset(self):
        # Filter Document objects where current status ID is 7
        return Document.objects.filter(document_current_status_id=7)

    def list(self, request, *args, **kwargs):
        # Use the filtered queryset
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": True,
            "message": "List of documents with current status ID 7 retrieved successfully",
            "data": serializer.data
        })






