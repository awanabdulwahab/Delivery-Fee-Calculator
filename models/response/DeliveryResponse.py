from dataclasses import dataclass


@dataclass
class DeliveryResponse:
    delivery_fee: int

    def to_dict(self):
        return {'delivery_fee': self.delivery_fee}
