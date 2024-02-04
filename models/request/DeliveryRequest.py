from dataclasses import dataclass
from datetime import datetime

@dataclass
class DeliveryRequest:
    cart_value: int
    delivery_distance: int
    number_of_items: int
    time: int
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            cart_value=data.get('cart_value'),
            delivery_distance=data.get('delivery_distance'),
            number_of_items=data.get('number_of_items'),
            time=data.get('time')
        )

    @staticmethod
    def validate_input_data(data):
        if not isinstance(data, dict):
            raise TypeError('Input data must be a dictionary')

        required_fields = ['cart_value', 'delivery_distance', 'number_of_items', 'time']
        # Get the list of keys missing from the input data
        missing_fields = [field for field in required_fields if field not in data]
        for field in required_fields:
            if field not in data:
                raise ValueError(f'{missing_fields} is required')

        if not isinstance(data['cart_value'], int) or data['cart_value'] < 0:
            return False, "Invalid cart value. It should be a non-negative integer."

        if not isinstance(data['delivery_distance'], int) or data['delivery_distance']<= 0:
            return False, "Invalid delivery distance. It should be a non-negative integer or greater than 0."

        if not isinstance(data['number_of_items'], int) or data['number_of_items']<= 0:
            return False, "Invalid number of items. It should be a non-negative integer or greater than 0."

        try:
            datetime.strptime(data['time'], "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            return False, "Incorrect time format. It should be YYYY-MM-DDTHH:MM:SSZ"

        return True, "Input data is valid"
