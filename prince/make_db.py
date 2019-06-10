#!/usr/bin/env python3
''' This script makes the necessary tables in the db. '''

import sqlite3

conn = sqlite3.connect('nasdaq.db')
c = conn.cursor()


def makeTables():
    c.execute(''' CREATE TABLE IF NOT EXISTS users(
        email TEXT PRIMARY KEY, password TEXT, account_balance INTEGER, user_type TEXT)
    ''')

    c.execute(''' CREATE TABLE IF NOT EXISTS trades(
        email TEXT, ticker TEXT, stocks INTEGER )
    ''')

    c.execute(''' CREATE TABLE IF NOT EXISTS stock_price(
        ticker TEXT, price INTEGER )
    ''')

    c.execute('''INSERT INTO users (email, password, account_balance, user_type) VALUES (?, ?, ?, ?)''',
        ('admin@nasdaq.com', '$2b$12$bgYzzSbpaMI1h15sxdu6IuVsZqaUu5zE2jkfeAFEnsid5iFmFxuKe', 0, 'admin'))
    
    c.execute('''INSERT INTO users (email, password, account_balance, user_type) VALUES (?, ?, ?, ?)''',
        ('user1@nasdaq.com', '$2b$12$bgYzzSbpaMI1h15sxdu6IuVsZqaUu5zE2jkfeAFEnsid5iFmFxuKe', 1000000, 'user'))
    
    c.execute('''INSERT INTO users (email, password, account_balance, user_type) VALUES (?, ?, ?, ?)''',
        ('user2@nasdaq.com', '$2b$12$bgYzzSbpaMI1h15sxdu6IuVsZqaUu5zE2jkfeAFEnsid5iFmFxuKe', 1000000, 'user'))
    
    c.execute('''INSERT INTO users (email, password, account_balance, user_type) VALUES (?, ?, ?, ?)''',
        ('user3@nasdaq.com', '$2b$12$bgYzzSbpaMI1h15sxdu6IuVsZqaUu5zE2jkfeAFEnsid5iFmFxuKe', 1000000, 'user'))
    
    conn.commit()
    c.close()
    conn.close()


if __name__ == "__main__":
    makeTables()