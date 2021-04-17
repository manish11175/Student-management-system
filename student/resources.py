
from import_export import resources
from.models import Student


class StudentResouce(resources.ModelResource):
    class meta:
        model=Student