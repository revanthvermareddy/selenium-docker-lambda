##################################################################
# -- setup base OS Image and args --
ARG base_os_img=python:3.9
FROM public.ecr.aws/lambda/${base_os_img}
##################################################################

##################################################################
# -- installing dependencies --

# install necessary utilities
RUN yum install -y \
    wget \
    tar \
    gzip \
    bzip2 \
    gtk3 \
    alsa-lib \
    dbus-glib

# install geckodriver
COPY geckodriver-install.sh  /tmp/geckodriver-install.sh
RUN sh /tmp/geckodriver-install.sh

# install linux firefox binary
RUN FIREFOX_SETUP=firefox-setup.tar.bz2 && \
    yum -y remove firefox && \
    wget -O ${FIREFOX_SETUP} "https://download.mozilla.org/?product=firefox-latest&os=linux64" && \
    tar xjf ${FIREFOX_SETUP} -C /opt/ && \
    ln -s /opt/firefox/firefox /usr/bin/firefox && \
    rm ${FIREFOX_SETUP}

##################################################################

##################################################################
# -- copying the source code and installing dependencies --

# install the function's dependencies using file requirements.txt from the project folder
COPY requirements.txt  /tmp/requirements.txt
RUN python -m pip install --upgrade pip && \
    python -m pip install -r /tmp/requirements.txt

# copying source code to default "LAMBDA_TASK_ROOT=/var/task" as the work dir
COPY app/lambda_function.py ${LAMBDA_TASK_ROOT}

# Create a non-root user with an explicit UID and add permission to access the /var/task folder
# For more info, please refer to https://code.visualstudio.com/docs/containers/troubleshooting#_running-as-a-nonroot-user
RUN /usr/sbin/adduser -u 5678 appuser && chown -R appuser ${LAMBDA_TASK_ROOT}
USER appuser

# Set the CMD to your handler
CMD ["lambda_function.lambda_handler"]

##################################################################