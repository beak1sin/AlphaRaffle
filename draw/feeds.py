from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Shoe

class LatestShoesFeed(Feed):
    title = "Latest Shoes"
    link = "/shoes/"
    description = "Updates on the latest shoes."

    def items(self):
        return Shoe.objects.order_by('-id')[:20]

    def item_title(self, item):
        return item.shoename
    
    def item_guid(self, item):
        return item.serialno

    # datetime 때문에 오류발생
    # def item_pubdate(self, item):
    #     return item.pubdate.strftime('')

    def item_description(self, item):
        return item.shoedetail

    def item_link(self, item):
        # return reverse('draw:detail', args=[item.pk])
        serialno = item.serialno
        return f'/auth/details/?serialnum={serialno}'