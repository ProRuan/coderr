# Third-party suppliers
from django.contrib import admin

# Local imports
from .models import Offer, OfferDetail


admin.site.register(Offer)
admin.site.register(OfferDetail)
