from rest_framework import serializers
from .models import Site


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ('id', 'user', 'name', 'url')
        read_only_fields = ('id', 'user')
