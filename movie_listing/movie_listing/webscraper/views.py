from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response

from ..sources.serializers import SourceSerializer
from ..sources.models import Source

from .spiders.chrome_driver import ChromeDriver

from json import dumps


class WebScraperViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows scrapy movie data from a source (website).
    """
    queryset = Source.objects.values()
    serializer_class = SourceSerializer
    
    def retrieve(self, request, *args, **kwargs):
        value = self.queryset[0]

        if value['name'] == 'ingresso.com':

            # XPATS to lead to the target web page.
            xpaths = ['//*[@id="header"]/div[2]/div/div/div/nav/ul/li[2]/a']

            website = ChromeDriver(url=value['url'], xpath_list=xpaths)
            website.start()

            website.quit(sleep_seconds=5)

        return Response(dumps({"status": "OK"}))
