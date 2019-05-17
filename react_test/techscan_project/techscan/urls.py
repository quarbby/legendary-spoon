from rest_framework import routers
from rest_framework.routers import SimpleRouter
# from .api import ZhihuViewSet
from techscan import views
from .views import ZhihuDocumentView
from django.conf.urls import url, include



router = routers.DefaultRouter()
router.register(r'zhihu', ZhihuDocumentView, base_name='ZhihuDocument')

urlpatterns = [
    url(r'^', include(router.urls))
]
# urlpatterns = router.urls

# app_name = 'techscan' 

# router = SimpleRouter()
# router.register(
#     prefix=r'',
#     base_name='techscan',
#     viewset=views.ZhihuDocumentView
# )
# urlpatterns = router.urls