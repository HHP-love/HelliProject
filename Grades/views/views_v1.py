# from rest_framework import viewsets
# from django_filters import rest_framework as filters
# from rest_framework.filters import SearchFilter
# from rest_framework import permissions
# from drf_spectacular.utils import extend_schema, OpenApiParameter
# from django_filters.rest_framework import DjangoFilterBackend
# from Grades.models import *
# from Grades.serializers import *
# from Grades.filters import *  
# from Grades.permissions import *  


# class StudentViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
#     filter_backends = [filters.DjangoFilterBackend]
#     search_fields = ['grade', 'full_name']
#     permission_classes = [permissions.IsAuthenticated, IsAdminUserOnly]


# @extend_schema(
#     request=None,
#     responses=ClassroomSerializer,
#     parameters=[
#         OpenApiParameter('name', description='Filter by classroom name', required=False, type=str),
#     ],
#     description="Retrieve classroom details, including teachers and students, with optional filters."
# )
# class ClassroomViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Classroom.objects.all()
#     serializer_class = ClassroomSerializer
#     filter_backends = [filters.DjangoFilterBackend, SearchFilter]
#     filterset_fields = ['name']
#     search_fields = ['name', 'subject__name']
#     permission_classes = [permissions.IsAuthenticated]




# from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample

# # @extend_schema_view(
# #     list=extend_schema(
# #         summary="Retrieve a list of grades",
# #         description="Fetch a list of all grades with optional filters for student names and classroom.",
# #         parameters=[
# #             OpenApiParameter(name='Student__first_name', type=str, location='query', description='Filter by student first name'),
# #             OpenApiParameter(name='Student__last_name', type=str, location='query', description='Filter by student last name'),
# #             OpenApiParameter(name='classroom__name', type=str, location='query', description='Filter by classroom name')
# #         ],
# #         examples=[
# #             OpenApiExample(
# #                 name="Example Request",
# #                 description="Filter grades for students with last name 'Smith' in 'Math' classroom.",
# #                 value={"Student__last_name": "Smith", "classroom__name": "Math"}
# #             )
# #         ]
# #     ),
# #     retrieve=extend_schema(
# #         summary="Retrieve a single grade",
# #         description="Fetch details of a specific grade by its ID.",
# #     ),
# #     create=extend_schema(
# #         summary="Create a new grade",
# #         description="Add a new grade for a student in a specific classroom.",
# #     ),
# #     update=extend_schema(
# #         summary="Update an existing grade",
# #         description="Modify details of an existing grade record."
# #     ),
# #     destroy=extend_schema(
# #         summary="Delete a grade",
# #         description="Remove a grade record by its ID."
# #     )
# # )
# # @extend_schema(exclude=True)
# # class GradeViewSet(viewsets.ModelViewSet):
# #     # """
# #     # API endpoint for managing grades in the system.

# #     # This ViewSet provides full CRUD operations for grade records, including:
# #     # - Retrieving a list of grades (`GET /grades/`)
# #     # - Retrieving a specific grade by ID (`GET /grades/{id}/`)
# #     # - Creating a new grade (`POST /grades/`)
# #     # - Updating an existing grade (`PUT /grades/{id}/`, `PATCH /grades/{id}/`)
# #     # - Deleting a grade (`DELETE /grades/{id}/`)

# #     # **Features:**
# #     # - **Authentication Required**: Only authenticated users can access this endpoint.
# #     # - **Filtering**: Supports filtering grades by:
# #     #     - `student__first_name` (case-sensitive exact match on student's first name)
# #     #     - `student__last_name` (case-sensitive exact match on student's last name)
# #     #     - `student__national_code` (case-sensitive exact match on student's national code)
# #     #     - `classroom__name` (case-sensitive exact match on classroom name)

# #     # **Fields:**
# #     # - `id`: Unique identifier for the grade record.
# #     # - `student`: Reference to the student associated with this grade.
# #     # - `classroom`: Reference to the classroom where the grade was assigned.
# #     # - `grade_value`: The numeric or letter grade assigned.
# #     # - `created_at`: Timestamp indicating when the grade record was created.
# #     # - `updated_at`: Timestamp indicating when the grade record was last updated.

# #     # **Example Usage:**
# #     # - Retrieve grades for a student with the last name "Doe":
# #     #     ```
# #     #     GET /grades/?student__last_name=Doe
# #     #     ```
# #     # - Retrieve grades for a classroom named "Math 101":
# #     #     ```
# #     #     GET /grades/?classroom__name=Math 101
# #     #     ```

# #     # **Permissions:**
# #     # - Only authenticated users (`IsAuthenticated`) can access this ViewSet.

# #     # **Notes:**
# #     # - Ensure proper naming conventions in filters (e.g., field names are case-sensitive).
# #     # - Pagination may be applied if enabled in the project settings.
# #     # """
# #     queryset = Grade.objects.all()
# #     serializer_class = GradeSerializer
# #     filter_backends = [DjangoFilterBackend]
# #     filterset_fields = ['student__first_name', 'student__last_name', 'student__national_code', 'classroom__name']
# #     permission_classes = [permissions.IsAuthenticated]
