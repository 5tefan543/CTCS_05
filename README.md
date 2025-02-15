
# Table of Contents

1. [Research Context](#research-context)
2. [Code Sources](#code-sources)
3. [Prerequisites](#prerequisites)
4. [Building and Running the Docker Image](#building-and-running-the-docker-image)
5. [Why Ubuntu 14.04?](#why-ubuntu-1404)
6. [How the System Works](#how-the-system-works)
7. [Additional Notes](#additional-notes)

---

## Research Context

This repository collects code from multiple sources to provide a unified environment for exploring the findings of the following paper:

> **Title:** EnerJ: Approximate Data Types for Safe and General Low-Power Computation  
> **Authors:** Adrian Sampson, Wonsun Ahn, Jonathan Grier, Jason Clemons, and Dan Grossman  
> **DOI:** [https://doi.org/10.1145/1993498.1993518](https://doi.org/10.1145/1993498.1993518)

This repository was created for a **Proseminar at the University of Innsbruck** and is intended solely for **educational purposes**. It provides a comprehensive setup to replicate and explore the implementations and concepts described in the linked paper. By combining tools and frameworks, the repository helps understand approximate computing and type-checking systems.

---

## Code Sources

The repository collects and integrates code from the following sources:

- [Checker Runtime](https://github.com/sampsyo/checker-runtime): The runtime library for managing type-checking functionality.
- [EnerJ](https://github.com/sampsyo/enerj): A research project focusing on approximate computing, which includes annotations and tools for Java.
- [EnerJ Apps](https://github.com/sampsyo/enerj-apps): Applications designed to work with the EnerJ framework.

Additionally, this project includes an older version of the [Checker Framework](https://checkerframework.org) (version 1.3.1). The Checker Framework provides a powerful set of tools for extending the Java type system with custom annotations, helping ensure correctness through compile-time checks.

---

## Prerequisites

Before building and running the project, ensure that you have the following installed on your system:

- **Docker** (Installation instructions: [Docker Documentation](https://docs.docker.com/get-docker/))
- A machine with internet access to pull the Docker base image and dependencies.

---

## Building and Running the Docker Image

### 1. Clone the Repository

```bash
git clone https://github.com/5tefan543/CTCS_05.git
cd CTCS_05
```

### 2. Build the Docker Image

Use the included Dockerfile to build the image. The Dockerfile sets up the required Ubuntu environment with all necessary dependencies.

```bash
docker build -t ctcs05 .
```

This will:
- Pull the **Ubuntu 14.04** base image.
- Install **OpenJDK 7** and other required dependencies.
- Copy the project files into the container.
- Compile the Java code within the container.

### 3. Run the Container

Once the image is built, run it to use the project:

```bash
docker run -it ctcs05
```

This command starts the container and drops you into a shell where you can interact with the compiled project.

### 4. Test the System

After starting the Docker container, you can test the functionality of the project using the provided example applications. Follow these steps:

#### Navigate to the Example Applications
1. Inside the container, list the project directories:
   ```bash
   ls
   ```
   You should see the following directories:
   ```
   checker-framework  checker-runtime  enerj  enerj-apps
   ```

2. Change to the `enerj-apps` directory, which contains example applications:
   ```bash
   cd enerj-apps/
   ```

3. List the available applications:
   ```bash
   ls
   ```
   Example output:
   ```
   HelloWorld  collect.py  count.py  imagefill  jmeint  scimark2  sclc  simpleRaytracer  zxing
   ```

#### Compile and Run the Example Application
1. Navigate to the `HelloWorld` example:
   ```bash
   cd HelloWorld/
   ```

2. Compile the `HelloWorld.java` program using the EnerJ compiler:
   ```bash
   ../../enerj/bin/enerjc -Alint=simulation HelloWorld.java
   ```

3. Run the compiled program with the EnerJ runtime:
   ```bash
   ../../enerj/bin/enerj -noisy HelloWorld
   ```

   Example output:
   ```
   Loading PrecisionRuntimeRoot
   Initializing noisy EnerJ runtime.
      Constants file not found; using defaults.
      SRAM WF: 87096
      SRAM RU: 25118864
      float bits: 8
      double bits: 16
      DRAM decay: 100000
      timing error mode: 2
      timing error prob: 1.5
   (878+55)*10=9330
   ```

4. You can repeat the `enerj` command to observe the behavior of the approximate computing runtime:
   ```bash
   ../../enerj/bin/enerj -noisy HelloWorld
   ```

---

### Additional Testing Notes
- Modify the `HelloWorld.java` source file to experiment with other computations.
- Explore other example applications in the `enerj-apps` directory, such as `simpleRaytracer` or `scimark2`, to test more complex scenarios.
- Use the EnerJ compiler (`enerjc`) and runtime (`enerj`) to test your own Java programs that utilize approximate computing annotations.

---

## Why Ubuntu 14.04?

The CTCS_05 project requires **OpenJDK 7** due to its compatibility with the Java codebase. Unfortunately, OpenJDK 7 has been deprecated and is not available in modern Ubuntu versions. To resolve this, the container uses **Ubuntu 14.04**, which supports OpenJDK 7.

The decision to use Ubuntu 14.04 ensures:
- A stable and compatible environment for the project.
- Isolation of the legacy Java runtime, avoiding conflicts with modern systems.

---

## How the System Works

The Docker container handles all compilation and setup automatically:
- The Dockerfile installs OpenJDK 7 and any additional tools required for the type-checker to function.
- The project source code is copied into the container and compiled during the build process.
- The resulting executable can be used directly within the container.

You do not need to configure or install anything on your host machine beyond Docker. This simplifies setup and ensures consistency across different environments.

---

## Additional Notes

- **Troubleshooting:** If you encounter issues during the build or run process, ensure your Docker installation is up-to-date and has sufficient permissions.
- **Extensibility:** You can modify the `Dockerfile` to add new dependencies or adapt the system to other environments if needed.
- **Legacy Code Warning:** Since this project relies on older technologies (Ubuntu 14.04 and OpenJDK 7), it is recommended to use it only in controlled or educational settings.

For any issues, contributions, or feature requests, please open an issue on the [GitHub repository](https://github.com/5tefan543/CTCS_05/issues).
