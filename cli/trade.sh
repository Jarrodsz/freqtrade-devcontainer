#!/bin/bash

strat_type="NNTC"
exchange="binance"
market="usdt"
port=8080
cd /freqtrade
dir="/freqtrade/user_data/strategies"

files="${strat_type}_*.py"

# Loop through the first 10 files in the directory
for strategy_file in $(ls -1q $dir/$files | head -n 10); do
  # Use parameter substitution to remove the .py extension
  strategy=${strategy_file%.py}
  strategy=${strategy##*/}
  echo $strategy
  cat <<END
    -------------------------
    $(date +%F\ %T)
    Dry-run strategy:${strategy} for exchange:${exchange}
    on market:${market}
    with port:${port}
    -------------------------
END
  export FREQTRADE__API_SERVER__LISTEN_PORT="${port}"
  freqtrade trade --dry-run \
    --config "/freqtrade/user_data/config/default.json" \
    --config "/freqtrade/user_data/config/exchange/${exchange}.json" \
    --db-url "sqlite:////freqtrade/user_data/database/${exchange}/${strategy}_strategy.sqlite" \
    --logfile "/freqtrade/user_data/logs/${exchange}/${strategy}.log" \
    -s "${strategy}" &
  sleep 40
  if [ $port -eq 8080 ]; then
    ((port+=20))
  else
    ((port+=1))
  fi
done
