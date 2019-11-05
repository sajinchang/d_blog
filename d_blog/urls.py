"""d_blog URL Configuration

The `urlpatterns` list routes URLs to show_api. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function show_api
    1. Add an import:  from my_app import show_api
    2. Add a URL to urlpatterns:  url(r'^$', show_api.home, name='home')
Class-based show_api
    1. Add an import:  from other_app.show_api import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin

from show_api import apis
from show_api import handler_error
from xmy import views as gallery_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'mdeditor/', include('mdeditor.urls')),
    url(r'^test/$', apis.Test.as_view()),

    url(r'^$', apis.Index.as_view(), name='index'),
    url(r'^gallery/', include('xmy.urls', namespace='gallery')),
    url(r'^gallery/list/$', gallery_view.GalleryView.as_view(), name='gallery'),

    url(r'^blog/', include('blog.urls', namespace='blog')),

]
handler404 = handler_error.page_not_found
handler500 = handler_error.server_error

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]

    from django.conf.urls.static import static

    # 访问media文件
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
