# Deployment Steps for Delisted API

## Initial Server Setup
```bash
# SSH into your Ubuntu server
ssh user@your-server-ip

# Copy application files to server
scp -r ./* user@your-server-ip:~/delisted-api/

# SSH into server and run setup
ssh user@your-server-ip
cd ~/delisted-api
chmod +x setup_server.sh
./setup_server.sh

# Log out and back in for docker group changes
exit
ssh user@your-server-ip
```

## Deploy Application
```bash
cd ~/delisted-api
chmod +x deploy.sh
./deploy.sh
```

## SSL Setup
```bash
# Before running setup_ssl.sh, replace your-domain.com in nginx.conf
cd ~/delisted-api
chmod +x setup_ssl.sh
./setup_ssl.sh
```

## Open Firewall Ports
```bash
sudo ufw allow 80
sudo ufw allow 443
```

## Monitoring Commands
```bash
# View logs
docker-compose logs -f

# Check container status
docker-compose ps

# Restart application
docker-compose restart
```

## Update Application
```bash
git pull
docker-compose up --build -d
```

## Access Points
- HTTP: http://your-domain.com
- HTTPS: https://your-domain.com
- API endpoint: https://your-domain.com/api/delisted/{exchange}
- Documentation: https://your-domain.com/docs