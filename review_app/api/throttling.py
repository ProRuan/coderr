from rest_framework.throttling import UserRateThrottle


class ReviewThrottle(UserRateThrottle):
    scope = 'review'

    def allow_request(self, request, view):
        if request.method == 'GET':
            return True

        new_scope = 'review-' + request.method.lower()
        if new_scope in self.THROTTLE_RATES:
            self.scope = new_scope
            self.rate = self.get_rate()
            self.num_requests, self.duration = self.parse_rate(self.rate)

        return super().allow_request(request, view)
