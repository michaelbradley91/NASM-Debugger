FROM python:3.6

WORKDIR /app

# Install additional dependencies
RUN apt-get update && apt-get install -y build-essential nasm

# By copying over requirements first, we make sure that Docker will cache
# our installed requirements rather than reinstall them on every build
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Now copy in our code, and run it
COPY . /app

# Build the assembly to be debugged
RUN ./build-assembly.sh

CMD ["python", "start.py"]
