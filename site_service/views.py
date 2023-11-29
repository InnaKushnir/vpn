import urllib
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Site, SiteTransition
from .serializers import SiteSerializer
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def proxy_view(request, user_site_name):
    site = Site.objects.get(name=user_site_name)
    url = site.url
    response = requests.get(url)

    from_site = request.META.get('HTTP_REFERER', 'Unknown')
    to_site = url
    user = site.user
    site_trans = SiteTransition.objects.create(user=user, from_site=from_site, to_site=to_site)
    if response.status_code == 200:
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')

        prefix = f"/api/proxy/{user_site_name}/"
        for a_tag in soup.find_all('a'):
            href = a_tag.get('href')

            if href and href.startswith('/'):
                href = href[1:]

            if href and not href.startswith(prefix) and not href.startswith('http'):
                href = href.rstrip('/')
                a_tag['href'] = f"{prefix}{href}"

        modified_content = soup.prettify(formatter=None)
        return HttpResponse(modified_content, content_type=response.headers['content-type'])
    else:
        return HttpResponse(status=response.status_code)


def proxy_view_with_path(request, user_site_name, routes_on_original_site):
    site = Site.objects.get(name=user_site_name)
    url = f"{site.url}/{routes_on_original_site}"
    print(url)
    response = requests.get(url)

    from_site = request.META.get('HTTP_REFERER', 'Unknown')
    to_site = url
    user = site.user
    site_trans = SiteTransition.objects.create(user=user, from_site=from_site, to_site=to_site)


    if response.status_code == 200:
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')

        prefix = f"/api/proxy/{user_site_name}/"
        for a_tag in soup.find_all('a'):
            href = a_tag.get('href')

            if href and href.startswith('/'):
                href = href[1:]

            if href and not href.startswith(prefix) and not href.startswith('http'):
                href = href.rstrip('/')
                a_tag['href'] = f"{prefix}{href}"

            # if href and not href.startswith('http'):
            #     parsed_url = urlparse(href)
            #     path = parsed_url.path  # Отримуємо шлях URL
            #
            #     if path.startswith('/'):
            #         path = path[1:]  # Видаляємо початковий '/'
            #
            #     # Перетворюємо URL в потрібний вигляд
            #     # Наприклад, лише шлях URL без домену та параметрів
            #     modified_href = f"{prefix}{path}"
            #     a_tag['href'] = modified_href

        modified_content = soup.prettify(formatter=None)
        return HttpResponse(modified_content, content_type=response.headers['content-type'])
    else:
        return HttpResponse(status=response.status_code)


class SiteListView(generics.ListAPIView):
    serializer_class = SiteSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return Site.objects.filter(user=self.request.user)


class SiteCreateView(generics.CreateAPIView):
    serializer_class = SiteSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SiteUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = SiteSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return Site.objects.filter(user=self.request.user)


class SiteDeleteView(generics.DestroyAPIView):
    serializer_class = SiteSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return Site.objects.filter(user=self.request.user)