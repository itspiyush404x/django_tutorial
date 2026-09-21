from functools import wraps
from django.core.cache import cache
from django.http import JsonResponse


def rate_limit_fixed_window(max_requests=10, window=60):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            ip = request.META.get("REMOTE_ADDR")

            if not ip:
                return JsonResponse(
                    {"error": "Unable to identify client."},
                    status=400
                )

            cache_key = f"rate_limit:{view_func.__module__}:{view_func.__name__}:{ip}"

            try:
                count = cache.incr(cache_key)
            except ValueError:
                cache.add(cache_key, 1, timeout=window)
                count = 1

            if count > max_requests:
                # retry_after = window

                response = JsonResponse(
                    {
                        "error": "Too many requests. Try again later."
                    },
                    status=429
                )

                # response["Retry-After"] = retry_after
                # response["X-RateLimit-Limit"] = max_requests
                # response["X-RateLimit-Remaining"] = 0

                return response

            response = view_func(request, *args, **kwargs)

            # response["X-RateLimit-Limit"] = max_requests
            # response["X-RateLimit-Remaining"] = max(
            #     0,
            #     max_requests - count
            # )

            return response

        return wrapper

    return decorator




def rate_limit_sliding_window(max_requests=10, window=60):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            ip = request.META.get("REMOTE_ADDR")

            if not ip:
                return JsonResponse(
                    {"error": "Unable to identify client."},
                    status=400
                )

            cache_key = f"rate_limit:{view_func.__module__}:{view_func.__name__}:{ip}"

            import time
            now = time.time()

            timestamps = cache.get(cache_key, [])
            imestamps = [
                timestamp
                for timestamp in timestamps
                if now - timestamp < window]

            if len(timestamps) >= max_requests:
                return JsonResponse({"error":"Too many request, try again!"}, status=429)
            
            

            timestamps.append(now)

            cache.set(cache_key, timestamps, timeout=window)
            
            return view_func(request, *args, *kwargs)
        
        return wrapper

    return decorator



