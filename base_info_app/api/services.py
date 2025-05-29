# Third-party suppliers
from django.db.models import Avg

# Local imports
from auth_app.models import CustomUser
from offer_app.models import Offer
from review_app.models import Review


class BaseInfoService:
    """
    Service to collect base info stats.
    """
    @staticmethod
    def get_info():
        """
        Get base info stats.
        """
        return {
            'review_count': Review.objects.count(),
            'average_rating': round(
                Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0.0, 1
            ),
            'business_profile_count': CustomUser.objects.filter(
                type='business'
            ).count(),
            'offer_count': Offer.objects.count(),
        }
