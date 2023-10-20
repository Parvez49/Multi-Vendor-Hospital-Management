from django_elasticsearch_dsl import Document, fields as es_fields
from django_elasticsearch_dsl.registries import registry

from .models import Hospital


@registry.register_document
class HospitalDocument(Document):
    id = es_fields.IntegerField()
    registration_no = es_fields.TextField()
    # hospital_name = es_fields.Text(
    #     analyzer="english"
    # )  # Use the "english" analyzer for text fields
    slug = es_fields.TextField()
    logo = es_fields.Object(multi=True)  # For nested objects, such as logo details
    # city = es_fields.TextField()
    # state = es_fields.TextField()
    postal_code = es_fields.TextField()
    country = es_fields.TextField()
    contact_number = (
        es_fields.Text()
    )  # Note: Using "Text" for phone number for partial matching
    website = es_fields.TextField()
    # description = es_fields.Text(analyzer="english")
    # additional_notes = es_fields.Text(analyzer="english")

    operating_hours = es_fields.TextField(analyzer="english")
    insurance_accepted = es_fields.TextField(analyzer="english")
    # facilities = es_fields.Text(analyzer="english")

    class Index:
        name = "hospitals"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = Hospital
        fields = [
            "hospital_name",
            "city",
            "state",
            "description",
            "additional_notes",
            "facilities",
        ]
