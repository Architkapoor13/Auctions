from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(AuctionListing)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Watchlist)