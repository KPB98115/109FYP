## Flask REST API for facial login, facial recognition, and object detection.
## Environment
* OS: Linux(Ubuntu 22.04.2 LTS)
* Python: 3.10.2
## Installation
* [Virualenv](https://pypi.org/project/virtualenv/) and [Pyenv](https://pypi.org/project/pyenv/) are used in my environment, I recommend doing so while testing the app.
  Install Virualenv and Pyenv via pip:  
  ```
  pip install virtualenv pyenv
  ```  
  Install python with Pyenv:  
  ```
  pyenv install -v 3.10.2
  ```  
  Switching python version:  
  ```
  $ pyenv [environment] 3.10.2 #environment = global, local, shell
  ```  
  Create a virtual environment with Pyenv:  
  ```
  virtualenv -p ~/.pyenv/versions/3.10.2/bin/python [your environment name]
  ```  
  Enter the virtual environment in MacOS:  
  ```
  source py39venv/bin/activate
  ```  
  Enter the virtual environment in Windows Shell:  
  ```
  .\Scripts\activate.bat
  ```  
  Enter the virtual environment in VScode PowerShell:  
  ```
  .\Scripts\activate.ps1
  ```  
  The name of the environment will appear in the terminal:  
  ```
  (VEname) $ ...
  ```  
* [face_recognition](https://github.com/ageitgey/face_recognition) is working on MacOS/Linux only, the facial detection API call would lead the app to crash when hosted on WindowOS.
* All required packages are in requirements.txt, enter `pip install -r requirement.txt` in your terminal to install all packages/dependencies.
* Make sure you pull Yolov5 to /109FYP/rest_api from GitHub by enter `git pull https://github.com/ultralytics/yolov5.git` before starting the flask app.
* We are hosting the API server on Ubuntu in WSL 2 and managed by Docker Desktop, see the document from https://learn.microsoft.com/zh-tw/windows/wsl/about
  After setting up the virtual machine, build the image with Dockerfile:  
  ```
  docker build -t [tag name of the image] .
  ```  
  It should take some time to build an image. Run the image after it is done:  
  ```
  docker run -p [5001:5000] flask_app
  # The cmd above will start the container on virtual machine port: 5000, and map to device port: 5001
  # The API URL would be "http://localhost:5001"
  ```
## Remarks
The API is hosted by Docker service, if there have any updates, please update the Dockerfile as well.
