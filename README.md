# CS50W Project 2: Auctions App

This repository contains my implementation of **Project 2: Auctions** for [CS50W](https://cs50.harvard.edu/web/), Harvard University's web programming course. The Auctions app is a web application inspired by popular e-commerce and auction platforms, allowing users to list items for bidding, place bids, leave comments, and watch items of interest.

## Overview

The Auctions App is built using Django, Python’s powerful web framework, and includes:
- **User Authentication**: Register, log in, and manage personal accounts.
- **Auction Listings**: Create, edit, and manage item listings.
- **Bidding System**: Place bids on listed items.
- **Watchlist**: Add items to a personal watchlist for quick access.
- **Commenting**: Leave comments on listings to interact with other users.

## Styling

The application’s user interface is styled using [Bootstrap](https://getbootstrap.com/), which provides a clean and responsive design across devices. Custom Bootstrap components are used to style forms, modals, and navigation elements, enhancing both usability and visual appeal.

## Setup

To run the Auctions App locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/auctions-app.git
   cd auctions-app
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Run the server**:
   ```bash
   python manage.py runserver
   ```

Open your browser and navigate to `http://127.0.0.1:8000` to view the Auctions App.

## Acknowledgments

This project builds upon the foundational code provided by CS50 staff as part of the course. Additional features and custom styling have been added according to my preferences to enhance the app's functionality and design.

## License

This project is licensed under the MIT License. Please adhere to CS50’s [academic honesty policy](https://cs50.harvard.edu/web/2023/honesty/) when using or referencing this code.
