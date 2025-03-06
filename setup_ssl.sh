#!/bin/bash

# Install Nginx and Certbot
sudo apt-get install -y nginx certbot python3-certbot-nginx

# Get SSL certificate (replace with your domain)
sudo certbot --nginx -d your-domain.com

# Copy Nginx configuration
sudo cp nginx.conf /etc/nginx/sites-available/delisted-api
sudo ln -s /etc/nginx/sites-available/delisted-api /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Test and reload Nginx
sudo nginx -t
sudo systemctl reload nginx