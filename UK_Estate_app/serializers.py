import json

from rest_framework import serializers

from UK_Estate_app.models import Sample, Property, Inquiry3


class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = "__all__"


class PropertySerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        # Call the original to_representation method to get the usual data
        ret = super(PropertySerializer, self).to_representation(instance)
        # Convert the right_image_url field from JSON string to Python list
        right_image_url = ret.get("right_image_url", "")
        if right_image_url:
            try:
                ret["right_image_url"] = json.loads(right_image_url)
            except json.JSONDecodeError:
                ret["right_image_url"] = []
        return ret

    class Meta:
        model = Property
        fields = "__all__"


class PropertyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"


from rest_framework import serializers


class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry3
        fields = "__all__"
