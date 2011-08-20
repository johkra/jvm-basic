all: clean
	./runtests.sh
clean:
	rm -f tests/*.class tests/*.output
