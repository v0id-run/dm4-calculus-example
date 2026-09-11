FROM blang/latex

RUN apt-get -y update && apt-get -y install curl
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get -y install python3 && apt-get -y install nodejs 
RUN curl https://github.com/jgm/pandoc/releases/download/2.7.3/pandoc-2.7.3-linux.tar.gz --location > pandoc-2.7.3.tar.gz && tar -xzvf  pandoc-2.7.3.tar.gz && mv pandoc-2.7.3/bin/* /usr/bin

