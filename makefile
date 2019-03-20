all: main.py display.py draw.py matrix.py parser.py
	python main.py

run: main.py display.py draw.py matrix.py parser.py
	python main.py

alt: alt.py display.py draw.py matrix.py parser.py
	python alt.py

clean:
	rm -f *.pyc
	rm -f *~
	rm -f *.png
