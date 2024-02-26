## Env setting

### BigDL for CPU - Conda
  ```sh
  conda create -n llm python=3.9 # recommend to use Python 3.9
  conda activate llm
  pip install --pre --upgrade bigdl-llm[all] # install the latest bigdl-llm nightly build with 'all' option
  ```

### BigDL for Intel GPU - Conda
  ```sh
  conda create -n llm-gpu python=3.9 # recommend to use Python 3.9
  conda activate llm-gpu
  # below command will install intel_extension_for_pytorch==2.1.10+xpu as default
  pip install --pre --upgrade bigdl-llm[xpu] -f https://developer.intel.com/ipex-whl-stable-xpu
  ```

### Python venv for OpenVINO
  ```sh
  python3 -m venv venv_ov
  source venv_ov/bin/activate
  pip install -q --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt
  ```
