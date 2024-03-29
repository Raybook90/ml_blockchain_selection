# ML-based Blockchain Selection

This is a Machine Learning based Blockchain Selection prototype that can be used either through a GUI or in conjunction with the Policy-based Blockchain Selection Framework, PleBeuS [[1]](#1).

Follow the installation steps to setup the Flask Application that offers an API endpoint and a GUI to access the ML models. The GUI is accessible through http://localhost:5000/.

To use the ML-based solution in conjunction with PleBeuS, PleBeuS needs to be installed as well. The source code of the extended version of the framework with the integrated ML functionality can be found [here](https://github.com/Raybook90/PleBeuS-Integration).

## Installation

Clone the repository and enter the project directory:
```
git clone https://github.com/Raybook90/ml_blockchain_selection.git 
cd ml_blockchain_selection 
```
Create a virtual environment:
```
$ python -m venv venv
```
Activate the virtual environment:
```
$ venv\Scripts\activate (Windows)
or
$ source venv/bin/activate (Linux, macOS)
```
Install dependencies:
``` 
(venv) $ pip install -r requirements.txt
```
Run app.py
```
$ python app.py
```
Deactivate the virtual environment:
```
$ deactivate
```

## References
<a id="1">[1]</a> 
Scheid, E., Lakic, D., Rodrigues, B., Stiller, B. (2020). 
PleBeuS: a Policy-based Blockchain Selection Framework. 
in: NOMS 2020 - 2020 IEEE/IFIP Network Operations and Management Symposium. pp. 1-8.
