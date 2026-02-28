from django.urls import path, include
from rest_framework import permissions
from rest_framework_nested import routers

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from .views import (
    UserViewSet, AuthorViewSet,
    CategoryViewSet, BookViewSet,
    BorrowViewSet
)


router = routers.DefaultRouter()

router.register('accounts', UserViewSet, basename='accounts')
router.register('authors', AuthorViewSet, basename='authors')
router.register('categories', CategoryViewSet, basename='categories')
router.register('books', BookViewSet, basename='book')
router.register('borrow', BorrowViewSet, basename='borrow')

account_router = routers.NestedDefaultRouter(router, r'accounts', lookup='account')
account_router.register(
    r'borrow', BorrowViewSet, basename='account-borrow'
)

author_router = routers.NestedDefaultRouter(router, r'authors', lookup='author')
author_router.register(
    r'books', BookViewSet, basename='author-books'
)

category_router = routers.NestedDefaultRouter(
    router, r'categories', lookup='category'
)
category_router.register(
    r'books', BookViewSet, basename='category-books'
)

schema_view = get_schema_view(
    openapi.Info(
        title='ReadLi App API',
        default_version='v1',
        decription='API documentation for ReadLi API',
        terms_of_service='https://www.localhost.com/terms/',
        contact=openapi.Contact(email='alexanderedim80@gmail.com'),
        license=openapi.License(name='MIT License')
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(account_router.urls)),
    path('', include(author_router.urls)),
    path('', include(category_router.urls)),

    # API Swagger Documentation
    path('swagger.json', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),

    # JWT Auth endpoints
    path('auth/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(),
         name='token-refresh')
]
