#!/bin/bash

# Stop and remove any orphaned containers
docker-compose -f docker-compose.yml down --remove-orphans

# Build and start the freqtrade_trade container in detached mode
docker-compose -f docker-compose.yml up --build -d freqtrade_trade

# Start the freqtrade container in detached mode
docker-compose -f docker-compose.yml up -d freqtrade

#docker exec -it freqtrade /bin/bash -c './user_data/trade.sh'
