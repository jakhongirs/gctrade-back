from rest_framework import serializers


class ImageSerializer(serializers.Serializer):
    def to_representation(self, instance):
        try:
            request = self.root.context["request"]
            return request.build_absolute_uri(instance.image.url)
        except (
            AttributeError,
            ValueError,
        ):  # image field has no file associated with it
            return None
        except KeyError:
            print(self.parent)
