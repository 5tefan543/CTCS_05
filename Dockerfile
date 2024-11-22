FROM ubuntu:14.04

# Set environment variables to avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install OpenJDK 7 and other necessary packages
RUN apt-get update && \
    apt-get install -y unzip && \
    apt-get install -y ant && \
    apt-get install -y openjdk-7-jdk

# Create a folder within the container
RUN mkdir -p /CTCS_05/

# Set the default working directory
WORKDIR /CTCS_05/

# Copy required files into the working directory
COPY checker-framework ./checker-framework
COPY checker-runtime ./checker-runtime
COPY enerj ./enerj
COPY enerj-apps ./enerj-apps

# Persist environment variables globally
ENV JSR308=/CTCS_05/checker-framework
ENV CHECKERS=$JSR308/checkers
ENV PATH=$CHECKERS/binary:$PATH

# Compile checker-runtime and enerj libraries
RUN cd checker-runtime && ant
RUN cd enerj && ant

# Set a command or script to run when the container starts
CMD ["bash"]