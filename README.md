# The Final Project of CSCI570

Two approaches for the String-Algin problem and their memory/time usage

---

## Before Running

Require Python version: 3.9.1 or newer.

Can't guarantee any lower version would be usable.

Check the `requirements.txt` which has listed every third-party package used in this project.

Get all package installed before running.

```shell
pip install -r requirements.txt
```

To be safer, you might need to create a virtual environment.

```shell
python3 -m venv venv
```

## Run The Project

```shell
python3 basic.py [inputFile = "input.txt"] [outputFile = "output.txt"]
python3 efficient.py [inputFile = "input.txt"] [outputFile = "output.txt"]
```

If `inputFile` is not given, the script will use `input.txt` in the same directory as the input file.

If `outputFile` is not given, the script will use `output.txt` in the same directory as the output file.

## Project Structure

```shell

proj
+-- algo.py             --> Containing main algorithm implementations, basic DP and Mem-Efficient
+-- input.txt           --> The input file used by strGen.py
+-- main.py             --> Entry functions
+-- requirements.txt    --> Package requirements
+-- IO.py               --> Handling input and output parts
+-- track.py            --> Memory tracker and CPU time tracker
+-- visualization.py    --> Visualize the time/Mem usage against problem size
+-- basic.py 		--> The entry of basic algo
+-- efficient.py 	--> The entry of memo-efficient algo

```
