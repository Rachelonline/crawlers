from __app__.utils.locations.redis_cache import get_place

# This is a set of names from the address components for locations.
#  If an ad is in any of these areas we'll do spam detection on it.
#  We don't do spam detection everywhere due to twilio costs

# A much better way to do this is checking the actual lat/lon, but we haven't
#  associated customers to a geo-region they care about
#   ...yet

CUSTOMER_ADMIN_AREAS = set({"King County",
                            "Franklin County",
                            "Tri-Cities",
                            "Benton County",
                            "Snohomish County",
                            "Toronto Division",
                            "Cook County",
                            "Santa Fe County",
                            "North Dakota",
                            "Hillsborough County",
                            "Jefferson County"})


def in_customer_region(message: dict) -> bool:
    location = message.get("location")
    if location is None:
        return False

    place = get_place(location.get("placeid"))
    if place is None:
        return False

    for addr_component in place.get("address_components", []):
        if addr_component.get("long_name") in CUSTOMER_ADMIN_AREAS:
            return True

    return False
