from django.db.models import Q, Model
from core.enums import Tuples
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST
)


class AddDelViewMixin:

    add_serializer: ModelSerializer = None

    def add_del_obj(self, obj_id, model: Model, query):
        obj = get_object_or_404(self.queryset, id=obj_id)
        serilalizer = self.add_serializer(
            obj,
            context={'request': self.request}
        )
        model_object = model.objects.filter(query & Q(user=self.request.user))

        if (self.request.method in Tuples.ADD_METHODS) and not model_object:
            model(None, self.request.user.id, obj.id).save()
            return Response(serilalizer.data, status=HTTP_201_CREATED)

        if (self.request.method in Tuples.DEL_METHODS) and model_object:
            model_object[0].delete()
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(status=HTTP_400_BAD_REQUEST)
