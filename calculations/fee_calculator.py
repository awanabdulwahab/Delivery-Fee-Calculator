from models.request.DeliveryRequest import DeliveryRequest
from enums.delivery_fee_rules import DeliveryFeeRule
from datetime import datetime


# calculate_cart_value_surcharge
def calculate_cart_value_surcharge(cart_value: int) -> int:
    # Check if the cart value is less than the threshold
    if cart_value < DeliveryFeeRule.cart_value_threshold.value:
        small_order_surcharge = 1000 - cart_value
    else:
        small_order_surcharge = 0
    return small_order_surcharge


# calculate_distance_fee
def calculate_distance_fee(delivery_distance: int) -> int:
    # Check if the delivery distance is less than the base rate delivery distance
    if delivery_distance <= DeliveryFeeRule.base_rate_delivery_distance.value:
        return DeliveryFeeRule.base_fee_1000_meters.value
    else:
        # Calculate the additional meters beyond the first 1000 meters
        additional_meters = max(0, delivery_distance - 1000)

        # Calculate the additional fee based on every 500 meters
        additional_fee_amount = ((additional_meters - 1) // 500 + 1) * DeliveryFeeRule.surcharge_per_500_meters.value

        # Calculate the total delivery fee
        total_fee = DeliveryFeeRule.base_fee_1000_meters.value + max(DeliveryFeeRule.surcharge_per_500_meters.value,
                                                                     additional_fee_amount)

        return total_fee


# calculate_number_of_items_surcharge
def calculate_number_of_items_surcharge(number_of_items: int) -> int:
    # Check if the number of items is more than the threshold
    if number_of_items > DeliveryFeeRule.bulk_item_minimum_threshold.value:
        # Calculate the additional items beyond the minimum threshold
        additional_items = number_of_items - DeliveryFeeRule.bulk_item_minimum_threshold.value
        # Calculate the surcharge based on the additional items
        item_surcharge = additional_items * DeliveryFeeRule.bulk_item_surcharge_base.value
        # Check if the number of items is more than the maximum threshold
        if number_of_items > DeliveryFeeRule.bulk_item_maximum_threshold.value:
            # Calculate the additional items beyond the maximum threshold
            item_surcharge += DeliveryFeeRule.bulk_item_surcharge.value
    else:
        item_surcharge = 0
    return item_surcharge


def is_rush_hour(order_time: str) -> bool:
    order_datetime = datetime.strptime(order_time, "%Y-%m-%dT%H:%M:%SZ")
    # Define the rush hour period in UTC
    rush_hour_start = datetime.strptime("15:00", "%H:%M").time()
    rush_hour_end = datetime.strptime("19:00", "%H:%M").time()

    return order_datetime.weekday() == 4 and rush_hour_start <= order_datetime.time() <= rush_hour_end


def apply_rush_hour_fee(delivery_fee: int, order_time: str) -> int:
    if is_rush_hour(order_time):
        delivery_fee *= DeliveryFeeRule.rush_hour_multiplier.value
    return delivery_fee


def calculate_delivery_fee(delivery_request: DeliveryRequest) -> int:
    # Initialize the delivery fee
    delivery_fee = 0
    # Check if the cart value is more than the free delivery threshold
    if delivery_request.cart_value >= DeliveryFeeRule.free_delivery_threshold.value:
        return delivery_fee
    # Calculate the delivery fee based on the cart value
    cart_value_surcharge = calculate_cart_value_surcharge(delivery_request.cart_value)

    # Calculate the delivery fee based on the distance
    distance_fee = calculate_distance_fee(delivery_request.delivery_distance)

    # Calculate the delivery fee based on the number of items
    number_of_items_surcharge = calculate_number_of_items_surcharge(delivery_request.number_of_items)

    # Calculate the total delivery fee
    delivery_fee = distance_fee + cart_value_surcharge + number_of_items_surcharge

    # Apply rush hour fee
    delivery_fee = apply_rush_hour_fee(delivery_fee, delivery_request.time)

    # Apply maximum delivery fee
    delivery_fee = min(delivery_fee, DeliveryFeeRule.maximum_delivery_fee.value)

    return delivery_fee
