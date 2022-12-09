FROM python:3.11
RUN touch ~/.bash_profile
RUN /bin/bash -c "$(curl -fsSL https://exaloop.io/install.sh)" || true
ENV PATH=/root/.codon/bin:$PATH

