import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from django.db.models import Count, Sum
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from user.models import User
from .models import Site, SiteTransition
from .serializers import SiteSerializer


def proxy_view(request, user_site_name):
    site = Site.objects.get(name=user_site_name)
    url = site.url
    response = requests.get(url)
    content_length = len(response.content)

    from_site = request.META.get('HTTP_REFERER', 'api/proxy/')
    to_site = url
    user = site.user
    site_trans = SiteTransition.objects.create(user=user, from_site=from_site,
                                               to_site=to_site, downloaded_content_size=content_length)
    if response.status_code == 200:
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')

        prefix = f"/api/proxy/{user_site_name}/"
        for tag in soup.find_all(['a', 'img', 'script', 'link']):

            if tag.has_attr('href'):
                href = tag['href']

                if href and not re.match(r'^(http|https|#|javascript:)', href):
                    if href.startswith('/'):
                        href = href[1:]

                    href = href.rstrip('/')
                    tag['href'] = f"{prefix}{href}"
                else:
                    parsed_href = urlparse(href)
                    parsed_url = urlparse(url)

                    if href and parsed_href.netloc == parsed_url.netloc:
                        relative_path = parsed_href.path.replace(parsed_url.path, '')
                        new_href = f"{prefix}{relative_path}"
                        tag['href'] = new_href
            else:
                if tag.has_attr('src'):
                    src = tag['src']

                    if src and not src.startswith(('http', 'https', '#', 'javascript:')):
                        src = src.rstrip('/')
                        tag['src'] = f"{prefix}{src}"
                    else:
                        parsed_src = urlparse(src)
                        parsed_url = urlparse(url)
                        if src and parsed_src.netloc == parsed_url.netloc:
                            relative_path = parsed_src.path.replace(parsed_url.path, '')
                            new_src = f"{prefix}{relative_path}"
                            tag['src'] = new_src

        modified_content = soup.prettify(formatter=None)
        return HttpResponse(modified_content, content_type=response.headers['content-type'])
    else:
        return HttpResponse(status=response.status_code)


def proxy_view_with_path(request, user_site_name, routes_on_original_site):
    site = Site.objects.get(name=user_site_name)
    url = f"{site.url}/{routes_on_original_site}"
    url_ = site.url

    response = requests.get(url)
    content_length = len(response.content)

    from_site = request.META.get('HTTP_REFERER', 'Unknown')
    to_site = url
    user = site.user
    site_trans = SiteTransition.objects.create(user=user, from_site=from_site,
                                               to_site=to_site, downloaded_content_size=content_length)

    if response.status_code == 200:
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')

        prefix = f"/api/proxy/{user_site_name}/"
        for tag in soup.find_all(['a', 'img', 'script', 'link']):

            if tag.has_attr('href'):
                href = tag['href']

                if href and href.startswith('/'):
                    href = href[1:]

                if href and not href.startswith(('http', 'https')):
                    href = href.rstrip('/')
                    tag['href'] = f"{prefix}{href}"

                else:
                    parsed_href = urlparse(href)
                    parsed_url = urlparse(url_)

                    if href and parsed_href.netloc == parsed_url.netloc:
                        relative_path = parsed_href.path.replace(parsed_url.path, '')
                        new_href = f"{prefix}{relative_path}"
                        tag['href'] = new_href
            else:
                if tag.has_attr('src'):
                    src = tag['src']

                    if src and src.startswith('/'):
                        src = src[1:]

                    if src and not src.startswith(('http', 'https')):
                        src = src.rstrip('/')
                        tag['src'] = f"{prefix}{src}"
                    else:
                        parsed_src = urlparse(src)
                        parsed_url = urlparse(url_)
                        if src and parsed_src.netloc == parsed_url.netloc:
                            relative_path = parsed_src.path.replace(parsed_url.path, '')
                            new_src = f"{prefix}{relative_path}"
                            tag['src'] = new_src

        modified_content = soup.prettify(formatter=None)
        return HttpResponse(modified_content, content_type=response.headers['content-type'])
    else:

        return HttpResponse(status=response.status_code)


class UserSiteStats(APIView):
    def get(self, request, id):
        user = get_object_or_404(User, id=id)

        site_transitions = (
            SiteTransition.objects
            .filter(user=user, from_site__startswith='http://127.0.0.1:8000/api/proxy/')
            .values('to_site')
            .annotate(
                total_transitions=Count('to_site'),
                total_content_size=Sum('downloaded_content_size')
            )
        )

        site_stats = []
        for site_transition in site_transitions:
            site_stats.append({
                'site_url': site_transition['to_site'],
                'total_transitions': site_transition['total_transitions'],
                'total_content_size': site_transition['total_content_size']
            })

        return JsonResponse({'user_site_stats': site_stats})


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
