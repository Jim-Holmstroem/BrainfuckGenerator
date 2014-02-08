interpreter:
	cython -a interpreter.pyx
	gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/usr/include/python2.7 -o interpreter.so interpreter.c

run:
	python -u run_example_code.py mandelbrot 32

clean:
	find . -type f -name "*.pyc" -exec rm -f {} \;
	find . -type f -name "*.pyo" -exec rm -f {} \;
	rm -f interpreter.c interpreter.so interpreter.html
	rm -rf __pycache__

test:
	nosetests -v -s
