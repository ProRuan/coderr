# 1. Standard libraries

# 2. Third-party suppliers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg

# 3. Local imports
from auth_app.models import CustomUser
from offer_app.models import Offer
from review_app.models import Review
from .serializers import BaseInfoSerializer


class BaseInfoAPIView(APIView):
    """
    GET /api/base-info/
    Returns overall platform statistics:
    - Total number of reviews (valuations)
    - Average rating (rounded to 1 decimal)
    - Total number of business users
    - Total number of offers
    """
    permission_classes = []  # public endpoint

    def get(self, request):
        # 1. Total reviews
        val_count = Review.objects.count()

        # 2. Average rating
        avg = Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0.0
        avg = round(avg, 1)

        # 3. Business user count
        biz_count = CustomUser.objects.filter(type='business').count()

        # 4. Offer count
        offer_count = Offer.objects.count()

        data = {
            'valuation_count': val_count,
            'average_rating': avg,
            'business_user_count': biz_count,
            'offer_count': offer_count,
        }
        serializer = BaseInfoSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


# # 1. Standard libraries

# # 2. Third-party suppliers
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.db.models import Avg

# # 3. Local imports
# from auth_app.models import CustomUser
# from offer_app.models import Offer
# from review_app.models import Review  # adjust import to your app name
# from .serializers import BaseInfoSerializer


# class BaseInfoView(APIView):
#     """
#     GET /api/base-info/
#     Returns overall counts and average rating for the platform.
#     """
#     permission_classes = []  # no authentication required

#     def get(self, request):
#         # Total number of valuations
#         val_count = Review.objects.count()
#         # Average rating rounded to one decimal
#         avg = Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0.0
#         avg = round(avg, 1)
#         # Number of business users
#         biz_count = CustomUser.objects.filter(type='business').count()
#         # Total number of offers
#         offer_count = Offer.objects.count()

#         data = {
#             'valuation_count': val_count,
#             'average_rating': avg,
#             'business_user_count': biz_count,
#             'offer_count': offer_count,
#         }
#         serializer = BaseInfoSerializer(data)
#         return Response(serializer.data, status=status.HTTP_200_OK)
