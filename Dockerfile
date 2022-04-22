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
RUN GECKODRIVER_VERSION=`curl https://github.com/mozilla/geckodriver/releases/latest | grep -Po 'v[0-9]+.[0-9]+.[0-9]+'` && \
    wget https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz && \
    tar -zxf geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz

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

# install the function's dependencies using file requirements.txt from your project folder
COPY requirements.txt  .

RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# copying source code to default "LAMBDA_TASK_ROOT=/var/task" as the work dir
COPY app/lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler
CMD ["lambda_function.lambda_handler"]

##################################################################