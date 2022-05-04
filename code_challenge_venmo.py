"""
Questions:
 

    1. Complete the `MiniVenmo.create_user()` method to allow our application to create new users.

    2. Complete the `User.pay()` method to allow users to pay each other. Consider the following: if user A is paying user B, user's A balance should be used if there's enough balance to cover the whole payment, if not, user's A credit card should be charged instead.

    3. Venmo has the Feed functionality, that shows the payments that users have been doing in the app. If Bobby paid Carol $5, and then Carol paid Bobby $15, it should look something like this
   

    Bobby paid Carol $5.00 for Coffee
    Carol paid Bobby $15.00 for Lunch

    Implement the `User.retrieve_activity()` and `MiniVenmo.render_feed()` methods so the MiniVenmo application can render the feed.

    4. Now users should be able to add friends. Implement the `User.add_friend()` method to allow users to add friends.
    5. Now modify the methods involved in rendering the feed to also show when user's added each other as friends.
"""

"""
MiniVenmo! Imagine that your phone and wallet are trying to have a beautiful
baby. In order to make this happen, you must write a social payment app.
Implement a program that will feature users, credit cards, and payment feeds.
"""

import re
import unittest
import uuid


class UsernameException(Exception):
    pass


class PaymentException(Exception):
    pass


class CreditCardException(Exception):
    pass


class Payment:
    def __init__(self, amount, actor, target, note):
        self.id = str(uuid.uuid4())
        self.amount = float(amount)
        self.actor = actor
        self.target = target
        self.note = note


class User:
    def __init__(self, username):
        self.credit_card_number = None
        self.balance = 0.0
        self.activity = []

        if self._is_valid_username(username):
            self.username = username
        else:
            raise UsernameException("Username not valid.")

    def add_to_activity(self, message):
        self.activity.append(message)

    # NOTE: This is called 'retrieve_activity' in the question details above.
    def retrieve_feed(self):
        return self.activity

    def add_friend(self, new_friend):
        # TODO: add code here
        pass

    def add_to_balance(self, amount):
        self.balance += float(amount)

    def add_credit_card(self, credit_card_number):
        if self.credit_card_number is not None:
            raise CreditCardException("Only one credit card per user!")

        if self._is_valid_credit_card(credit_card_number):
            self.credit_card_number = credit_card_number

        else:
            raise CreditCardException("Invalid credit card number.")

    def pay(self, target, amount, note):
        try:
            if self.balance >= amount:
                self.pay_with_balance(target, amount, note)

            else:
                self.pay_with_card(target, amount, note)

        except PaymentException:
            raise

    def pay_with_card(self, target, amount, note):
        amount = float(amount)

        if self.username == target.username:
            raise PaymentException("User cannot pay themselves.")

        elif amount <= 0.0:
            raise PaymentException("Amount must be a non-negative number.")

        elif self.credit_card_number is None:
            raise PaymentException("Must have a credit card to make a payment.")

        self._charge_credit_card(self.credit_card_number)
        payment = Payment(amount, self, target, note)
        target.add_to_balance(amount)

        return payment

    def pay_with_balance(self, target, amount, note):
        amount = float(amount)

        if self.username == target.username:
            raise PaymentException('User cannot pay themselves.')

        elif amount <= 0.0:
            raise PaymentException('Amount must be a non-negative number.')

        elif self.balance < amount:
            raise PaymentException('Insufficient balance to make payment.')

        payment = Payment(amount, self, target, note)
        target.add_to_balance(amount)
        self.add_to_balance(-amount)

        return payment

    def _is_valid_credit_card(self, credit_card_number):
        return credit_card_number in ["4111111111111111", "4242424242424242"]

    def _is_valid_username(self, username):
        return re.match("^[A-Za-z0-9_\\-]{4,15}$", username)

    def _charge_credit_card(self, credit_card_number):
        # magic method that charges a credit card thru the card processor
        pass


class MiniVenmo:
    def create_user(self, username, balance, credit_card_number):
        try:
            new_user = User(username)
            new_user.add_credit_card(credit_card_number)
            new_user.add_to_balance(balance)
        except UsernameException:
            raise

        return new_user

    def render_feed(self, feed):
        # Bobby paid Carol $5.00 for Coffee
        # Carol paid Bobby $15.00 for Lunch
        # TODO: add code here
        pass

    @classmethod
    def run(cls):
        venmo = cls()

        bobby = venmo.create_user("Bobby", 5.00, "4111111111111111")
        carol = venmo.create_user("Carol", 10.00, "4242424242424242")

        try:
            # should complete using balance
            bobby.pay(carol, 5.00, "Coffee")

            # should complete using card
            carol.pay(bobby, 15.00, "Lunch")
        except PaymentException as e:
            print(e)

        feed = bobby.retrieve_feed()
        venmo.render_feed(feed)

        bobby.add_friend(carol)


class TestUser(unittest.TestCase):
    def test_this_works(self):
        with self.assertRaises(UsernameException):
            raise UsernameException()

    def test_pay_with_balance_success(self):
        alice = User("Alice")
        alice.add_to_balance(5.00)

        bobby = User("Bobby")
        bobby.add_to_balance(10.00)

        alice.pay_with_balance(bobby, 5.00, "Present")
        self.assertEqual(alice.balance, 0.00)
        self.assertEqual(bobby.balance, 15.00)

    def test_pay_with_balance_failure(self):
        alice = User("Alice")
        alice.add_to_balance(5.00)

        bobby = User("Bobby")
        bobby.add_to_balance(10.00)

        with self.assertRaises(PaymentException) as exception1:
            alice.pay_with_balance(alice, 1.00, "Savings")

        self.assertTrue("User cannot pay themselves." in str(exception1.exception))

        with self.assertRaises(PaymentException) as exception2:
            alice.pay_with_balance(bobby, -15.00, "Dinner")

        self.assertTrue("Amount must be a non-negative number." in str(exception2.exception))

        with self.assertRaises(PaymentException) as exception3:
            alice.pay_with_balance(bobby, 15.00, "Dinner")

        self.assertTrue("Insufficient balance to make payment." in str(exception3.exception))

    def test_pay_success(self):
        alice = User("Alice")
        alice.add_credit_card("4111111111111111")
        alice.add_to_balance(5.00)

        bobby = User("Bobby")
        bobby.add_credit_card("4242424242424242")
        bobby.add_to_balance(10.00)

        # Pay Bob with balance:
        alice.pay(bobby, 5.00, "Present")
        self.assertEqual(alice.balance, 0.00)
        self.assertEqual(bobby.balance, 15.00)

        # Pay Alice with credit card:
        bobby.pay(alice, 30.00, "Shoes")
        self.assertEqual(bobby.balance, 15.00)
        self.assertEqual(alice.balance, 30.00)
        
    def test_pay_failures(self):
        alice = User("Alice")
        alice.add_to_balance(5.00)

        bobby = User("Bobby")
        bobby.add_credit_card("4242424242424242")
        bobby.add_to_balance(10.00)

        # Must raise a PaymentException because the user doesn't have enough balance,
        # and also doesn't have a credit card:
        with self.assertRaises(PaymentException) as exception1:
            alice.pay(bobby, 15.00, "Dinner")

        self.assertTrue("Must have a credit card to make a payment." in str(exception1.exception))

        with self.assertRaises(PaymentException) as exception2:
            alice.pay(bobby, -15.00, "Dinner")

        self.assertTrue("Amount must be a non-negative number." in str(exception2.exception))

        with self.assertRaises(PaymentException) as exception3:
            alice.pay(alice, 15.00, "Dinner")

        self.assertTrue("User cannot pay themselves." in str(exception3.exception))

    def test_add_activity(self):
        alice = User('Alice')
        message = 'Alice has registered in Venmo'
        alice.add_to_activity(message)
        self.assertIn(message, alice.activity)

    def test_retrieve_feed(self):
        test_user = User('TestUser')
        test_feed_items = [
            'TestUser registered on 2022-05-05',
            'TestUser added Interviewer as a friend'
            'TestUser paid Wife $5.00 for Lunch',
        ]
        for feed_item in test_feed_items:
            test_user.add_to_activity(feed_item)

        test_user_feed =  test_user.retrieve_feed()
        self.assertCountEqual(test_feed_items, test_user_feed)

        for idx, feed_item in enumerate(test_feed_items):
            self.assertEqual(feed_item, test_user_feed[ idx ])

class TestMiniVenmo(unittest.TestCase):

    def test_create_user(self):
        carlos_user_details = {
            "username": "Carlos",
            "balance": 23.00,
            "credit_card_number": "4111111111111111",
        }
        mv = MiniVenmo()
        carlos_user = mv.create_user(**carlos_user_details)
        self.assertEqual(carlos_user_details["username"], carlos_user.username)
        self.assertEqual(carlos_user_details["balance"], carlos_user.balance)
        self.assertEqual(carlos_user_details["credit_card_number"], carlos_user.credit_card_number)

    def test_create_user_fail(self):
        wrong_user_details = {
            "username": "Car",  # Will fail because the username is too short.
            "balance": 23.00,
            "credit_card_number": "4111111111111111",
        }
        mv = MiniVenmo()
        with self.assertRaises(UsernameException):
            mv.create_user(**wrong_user_details)

    def test_functionality(self):
        mv = MiniVenmo()
        mv.run()

if __name__ == "__main__":
    unittest.main()
