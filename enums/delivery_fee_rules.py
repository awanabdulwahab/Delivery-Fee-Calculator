from enum import Enum


class DeliveryFeeRule(Enum):
    # Cart value threshold for small order surcharge
    cart_value_threshold = 10000

    # base rate delivery distance in meters
    base_rate_delivery_distance = 1000

    # Base fee for the first 1000 meters
    base_fee_1000_meters = 200

    # Surcharge per additional 500 meters after the first 1000 meters
    surcharge_per_500_meters = 100

    # Minimum fee
    minimum_fee = 100

    # Small order surcharge for cart value less than 10
    small_order_surcharge = 110

    bulk_item_minimum_threshold = 4

    bulk_item_maximum_threshold = 12

    bulk_item_surcharge_base = 50

    # Bulk item surcharge for more than 12 items
    bulk_item_surcharge = 120

    # Maximum delivery fee
    maximum_delivery_fee = 1500

    # Free delivery for cart value more than 200 euros
    free_delivery_threshold = 20000

    # Delivery fee multiplier for rush hour
    rush_hour_multiplier = 1.2
