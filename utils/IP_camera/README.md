<!-- ABOUT THE PROJECT -->
## About The Project

This is a reference for using a webcam as an IP camera.


<!-- GETTING STARTED -->
## Getting Started

Instructions on setting up your project locally.

### Python virtual env for server

  ```sh
  python3 -m venv venv_ipcam
  source venv_ipcam/bin/activate
  pip install -U pip
  ```

### Python virtual env for client

  ```sh
  python3 -m venv venv_ipcam
  source venv_ipcam/bin/activate
  pip install opencv-python
  ```

### Installation

  ```sh
  pip install -r requirements.txt
  ```

<!-- USAGE EXAMPLES -->
## Usage
### Server
  1. Webcam should be available at the server
  2. Run the python code.
    ```sh
    source venv_ipcam/bin/activate
    python3 server.py
    ```

### Client
  1. Check the IP address of the server
  2. Update the IP address from the `client.py`
  3. Run the python code.
    ```sh
    source venv_ipcam/bin/activate
    python3 client.py
    ```
