<!-- ABOUT THE PROJECT -->
## About The Project
This is a reference for google Text 2 Speech based on [here](https://gtts.readthedocs.io/en/latest/).


<!-- GETTING STARTED -->
## Getting Started

Instructions on setting up your project locally.

### Prerequisites

### Python virtual env

  ```sh
  python3 -m venv venv_gTTS
  source venv_gTTS/bin/activate
  pip install -U pip
  ```

### Installation

  ```sh
  pip install -r requirements.txt
  ```


<!-- USAGE EXAMPLES -->
## Usage

Run the python code.
  ```sh
  python3 test.py
  ```

### CLI command to check the supported languages

  ```sh
  gtts-cli --all
  ```

### SSML
https://cloud.google.com/docs/authentication/provide-credentials-adc#how-to
https://cloud.google.com/sdk/docs/install#deb
https://cloud.google.com/text-to-speech/docs/ssml

  ```sh
  pip install --upgrade google-cloud-texttospeech
  export GOOGLE_APPLICATION_CREDENTIALS="application_default_credentials.json"
  ```
