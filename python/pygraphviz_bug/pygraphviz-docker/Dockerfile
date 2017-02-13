FROM ubuntu:16.04
RUN apt-get update
RUN apt-get -y install apt-utils
RUN apt-get -y install git
RUN git clone https://github.com/pygraphviz/pygraphviz.git /root/pygraphviz
RUN apt-get -y install build-essential
RUN apt-get -y install python
RUN apt-get -y install python-dev
RUN apt-get -y install python-setuptools
RUN apt-get -y install autoconf
RUN easy_install pip
RUN pip install virtualenv tox tox-run-command
RUN apt-get -y install pkg-config
RUN apt-get -y install autogen autoconf libtool
RUN apt-get -y install byacc flex
RUN apt-get -y install bison
WORKDIR /root
ADD ./bug.py /root/pygraphviz/bug.py

CMD cd /root/graphviz; git clean -fx; ./autogen.sh; ./configure --enable-perl=no; make -j8; make -j8 install