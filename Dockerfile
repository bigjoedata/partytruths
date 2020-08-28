FROM python:3.7

RUN pip install virtualenv
ENV VIRTUAL_ENV=/venv
RUN virtualenv venv -p python3
ENV PATH="VIRTUAL_ENV/bin:$PATH"

WORKDIR /app
ADD ./app /app

# Install dependencies
RUN pip install -r requirements.txt

# copying all files over
COPY . /app

# Expose port 
#ENV PORT 8501
EXPOSE 8080

# streamlit-specific commands for config
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN mkdir -p /root/.streamlit

# Applies a custom index.html with Google Tag Manager added
COPY /stconfigs /root/.streamlit/

COPY ./stindex/index.html /usr/local/lib/python3.7/site-packages/streamlit/static
COPY ./app/favicon.png /usr/local/lib/python3.7/site-packages/streamlit/static

# cmd to launch app when container is run
CMD streamlit run app.py