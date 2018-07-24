# mssql-python-pyodbc
# Python runtime with pyodbc to connect to SQL Server
FROM ubuntu:16.04
USER root

# apt-get and system utilities
RUN apt-get update && apt-get install -y \
    curl apt-utils apt-transport-https debconf-utils gcc build-essential g++-5\
    && rm -rf /var/lib/apt/lists/*

# adding custom MS repository
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# install SQL Server drivers
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql unixodbc-dev

# install SQL Server tools
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y mssql-tools
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN /bin/bash -c "source ~/.bashrc"

#install Java JDK
RUN apt-get update;apt-get install -y openjdk-8-jdk-headless wget openssh-server tar vim

#ssh
RUN echo “root:training” | chpasswd
RUN sed -i ‘s/prohibit-password/yes/’ /etc/ssh/sshd_config
ADD ssh.tar /root/
RUN chown -R root:root /root/.ssh;chmod -R 700 /root/.ssh
RUN echo “StrictHostKeyChecking=no” >> /etc/ssh/ssh_config
RUN mkdir /var/run/sshd

# python libraries
RUN apt-get update && apt-get install -y \
    python-pip python-dev python-setuptools \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# install necessary locales
RUN apt-get update && apt-get install -y locales \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen
RUN pip install --upgrade pip

# install SQL Server Python SQL Server connector module - pyodbc
RUN pip install pyodbc

# install additional utilities
RUN apt-get update && apt-get install gettext nano vim -y

# add sample code
RUN mkdir /sample
ADD . /sample
WORKDIR /sample

CMD /bin/bash ./entrypoint.sh

#Startup #ssh
ADD start.sh 201 /

EXPOSE 22 8088 50070
CMD bash /start.sh
