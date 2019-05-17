from techscan.models import Zhihu
from rest_framework import viewsets, permissions
from .serializers import ZhihuSerializer

# Zhihu Viewset
class ZhihuViewSet(viewsets.ModelViewSet):
    queryset = Zhihu.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ZhihuSerializer