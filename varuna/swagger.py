from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Varuna API",
      default_version='v1',
      description="Varuna API Documentation",
      contact=openapi.Contact(email="masao.kiba426@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)
