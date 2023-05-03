#!/bin/bash

# This script runs the Freqtrade trading strategy
# both in a devcontainer or with docker-compose in a dry way

# Get the absolute path of the script's parent directory
SCRIPT_DIR="$(dirname "$(readlink -f "$1")")"
STRATEGIES_DIR="$SCRIPT_DIR/user_data/strategies"

echo "Strategies directory path: $STRATEGIES_DIR"

# Define default values for command-line arguments
EXCHANGE="binance"
MARKET="usdt"
PORT=8080
STRAT_TYPE="" # NNTC_
STRATEGY_FILTER="${STRAT_TYPE}*.py"

while getopts ":e:m:p:" opt; do
  case $opt in
    e) EXCHANGE="$OPTARG"
    ;;
    m) MARKET="$OPTARG"
    ;;
    p) PORT="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

if [[ -z "$EXCHANGE" || -z "$MARKET" || -z "$PORT" ]]; then
  echo "Usage: $0 -e EXCHANGE -m MARKET -p PORT"
  exit 1
fi



# Define functions
build_container() {
    docker build -f docker/Dockerfile -t freqtrade .
}

run_freqtrade() {
    strategy="$1"

    freqtrade_config="--config /freqtrade/user_data/config/default.json \
                      --config /freqtrade/user_data/config/exchange/${exchange}.json \
                      --db-url sqlite:////freqtrade/user_data/database/${exchange}/${strategy}_strategy.sqlite \
                      --logfile /freqtrade/user_data/logs/${exchange}/${strategy}.log \
                      -s ${strategy}"

    if [ "$VSCODE_REMOTE_CONTAINERS_SESSION" = "true" ]; then
        echo "You are inside a devcontainer CLI."
        freqtrade trade --dry-run ${freqtrade_config} &
    else
        echo "You are not inside a devcontainer CLI."
        build_container
        stop_container "freqtrade_${exchange}${i}"
        docker run -d \
            --name freqtrade_${exchange}${i} \
            -v ./user_data/config/default.json:/freqtrade/user_data/default.json \
            -v ./user_data/:/freqtrade/user_data \
            -v ./user_data/database/${exchange}_tradesv3.sqlite:/freqtrade/user_data/database/${exchange}_tradesv3.sqlite \
            freqtrade trade ${freqtrade_config}
    fi
}

stop_container() {
  local container_name="$1"
  if docker ps -a --format '{{.Names}}' | grep -q "$container_name"; then
    echo "Stopping and removing existing container $container_name..."
    docker stop "$container_name"
    docker rm "$container_name"
  else
    echo "No existing container found with name: $container_name"
  fi
}

# Main loop
i=1
for strategy_file in $(ls -1q $STRATEGIES_DIR/$STRATEGY_FILTER | head -n 10); do
    # Use parameter substitution to remove the .py extension
    strategy=${strategy_file%.py}
    strategy=${strategy##*/}
    echo $strategy
    cat <<END
    -------------------------
    $(date +%F\ %T)
    Run strategy:${strategy} for exchange:${EXCHANGE}
    on market:${MARKET}
    with port:${PORT}
    -------------------------
END

    export FREQTRADE__API_SERVER__LISTEN_PORT="${PORT}"

    # run the strategy
    run_freqtrade "$strategy"

    sleep 1
    if [ $PORT -eq 8080 ]; then
        ((PORT += 20))
    else
        ((PORT += 1))
    fi
    ((i++))
done
