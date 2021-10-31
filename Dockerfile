FROM continuumio/miniconda3:4.9.2

WORKDIR /app
RUN apt-get --allow-releaseinfo-change update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN conda create -n celebrity python=3.7
COPY env.yml .
RUN conda env update --name celebrity --file env.yml --prune

COPY . .

#CMD conda run -n wagon /bin/bash -c "python -u start.py &"
