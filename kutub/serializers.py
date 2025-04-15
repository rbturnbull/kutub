from rest_framework import serializers
from . import models


class ManuscriptSerializer(serializers.Serializer):
  class Meta:
    model = models.Manuscript
    fields = [
      "heading",
      "identifier",
      "alt_identifier",
      "url",
      "tags",
      "content_summary",
      "iiif_manifest_url",
      "physical_description_summary",
      "support_description",
      "catchwords",      
    ]