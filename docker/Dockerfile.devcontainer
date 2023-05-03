FROM freqtradeorg/freqtrade:develop

USER root


RUN apt-get update \
    && apt-get -y install zsh \
    && apt-get clean

RUN chsh -s $(which zsh) ftuser

# Install dependencies
COPY requirements-dev.txt /freqtrade/


RUN apt-get update \
    && apt-get -y install git mercurial sudo vim build-essential \
    && apt-get clean \
    && mkdir -p /home/ftuser/.vscode-server /home/ftuser/.vscode-server-insiders /home/ftuser/commandhistory \
    && echo "export PROMPT_COMMAND='history -a'" >> /home/ftuser/.bashrc \
    && echo "export HISTFILE=~/commandhistory/.bash_history" >> /home/ftuser/.bashrc \
    && chown ftuser:ftuser -R /home/ftuser/.local/ \
    && chown ftuser: -R /home/ftuser/

USER ftuser

RUN pip install --upgrade pip


# CUSTOM DEPS
#RUN curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh
#RUN sh Miniconda3-latest-Linux-aarch64.sh -b -p
#RUN pip install tensorflow-metal
#RUN conda install -c conda-forge -y pandas jupyter
#RUN conda install pytorch torchvision -c pytorch


RUN pip install tqdm quantstats
RUN pip install finta
RUN pip install prettytable
RUN pip install PyWavelets
RUN pip install simdkalman
RUN pip install pykalman
RUN pip install scipy
RUN pip install scikit-learn
RUN pip install xgboost

#RUN conda install -c apple tensorflow-deps
#RUN conda install -c conda-forge -y pandas jupyter
#RUN conda install pytorch torchvision -c pytorch

RUN pip install tensorflow
RUN pip install numpy

RUN pip install keras
RUN pip install darts
RUN pip install multiprocess


# Start the proxy
#CMD ["bash", "-c", "/freqtrade/user_data/cli/binance-proxy --disable-fake-candles"]
#CMD ["bash", "-c", "/freqtrade/user_data/start.sh"]

# Empty the ENTRYPOINT to allow all commands
ENTRYPOINT []
