"""
Personalized Trip Planner - Booking & Payment Service

Handles seamless booking via EMT inventory and payment processing. Stores confirmations in Firebase.
"""


class BookingPaymentService:
    def __init__(self, emt_client, firebase_client, payment_client):
        self.emt = emt_client
        self.firebase = firebase_client
        self.payment = payment_client

    def book(self, itinerary_id, payment_info):
        """
        Book itinerary via EMT inventory and process payment, store confirmation in Firebase.
        """
        booking_confirmation = self.emt.book(itinerary_id, payment_info)  # Replace with actual EMT API call
        payment_status = self.payment.process(payment_info)  # Replace with actual payment gateway integration
        self.firebase.save_booking_confirmation(itinerary_id, booking_confirmation)
        return booking_confirmation, payment_status
