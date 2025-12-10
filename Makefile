run: compile
	echo "============== Run =================="
	python ./src/__pycache__/main.cpython-313.pyc

debug:
	echo "=============== Debug ================="

compile:
	echo "============== Compile ================="
	python -m py_compile ./src/main.py

clear:
	rm -rf ./src/__pycache__/*
