# What this is

This is a code challenge presented to me for a Python Developer role.

# Problem statement

MiniVenmo! Imagine that your phone and wallet are trying to have a beautiful baby.

In order to make this happen, you must write a social payment app.

Implement a program that will feature users, credit cards, and payment feeds.

# Questions / Tasks

    1. Complete the `MiniVenmo.create_user()` method to allow our application to create new users.

    2. Complete the `User.pay()` method to allow users to pay each other. Consider the following: if user A is paying user B, user's A balance should be used if there's enough balance to cover the whole payment, if not, user's A credit card should be charged instead.

    3. Venmo has the Feed functionality, that shows the payments that users have been doing in the app. If Bobby paid Carol $5, and then Carol paid Bobby $15, it should look something like this

    Bobby paid Carol $5.00 for Coffee
    Carol paid Bobby $15.00 for Lunch

    Implement the `User.retrieve_activity()` and `MiniVenmo.render_feed()` methods so the MiniVenmo application can render the feed.

    4. Now users should be able to add friends. Implement the `User.add_friend()` method to allow users to add friends.
    5. Now modify the methods involved in rendering the feed to also show when user's added each other as friends.

# My approach

I'm trying to enforce TDD (Test Driven Development) in the code that I write, so I will mostly start off with tests of my code, then the actual code that passes those tests.

Whenever there's a change in functionality, I'll write the new test cases, then adapt the code to make those tests pass.

I tried not to get ahead of myself and add features before the tests. Hopefully the commit history serves as a way into my thought process.
