#!/bin/bash

# Install Nginx and Certbot
sudo apt-get install -y nginx certbot python3-certbot-nginx

# Copy Nginx configuration
sudo cp nginx.conf /etc/nginx/sites-available/delisted-api
sudo ln -s /etc/nginx/sites-available/delisted-api /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Test and reload Nginx
sudo nginx -t
sudo systemctl reload nginx

# Get SSL certificate
sudo certbot --nginx -d delisted.space --non-interactive --agree-tos --email your-email@example.com

# Final Nginx reload
sudo nginx -t
sudo systemctl reload nginx
