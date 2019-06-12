FROM nasm-debugger-base

WORKDIR /app

ARG XDG_RUNTIME_DIR
RUN mkdir $XDG_RUNTIME_DIR

# Install any new requirements in this image...
COPY requirements.txt /app/requirements.txt
RUN pip uninstall -r requirements.txt -y && pip install -r requirements.txt

# Now copy in our code, and run it
COPY . /app

# Build the assembly to be debugged
RUN ./build-assembly.sh

# Run the application
CMD python src/main/python/main.py
