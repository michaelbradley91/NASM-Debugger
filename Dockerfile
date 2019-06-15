FROM nasm-debugger-base

WORKDIR /app

ARG XDG_RUNTIME_DIR
RUN mkdir $XDG_RUNTIME_DIR

# Install any new requirements in this image...
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Now copy in our code, and run it
COPY ./src /app
COPY ./root /root

# Build the assembly to be debugged
RUN /root/build-assembly.sh

# Run the application
CMD python main/python/main.py
