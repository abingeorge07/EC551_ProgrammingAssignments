CC= g++ -std=c++17

# Links the object files to create an executable 
#checks if there are any changes
all: commandPrompt.o synthesisLib.o
	$(CC) commandPrompt.o synthesisLib.o -o run

# If there are changes to commandPrompt, re-compile .cpp
commandPrompt.o: commandPrompt.cpp synthesisLib.h
	$(CC) -c commandPrompt.cpp

# If there are changes to commandPrompt, re-compile .cpp
synthesisLib.o: synthesisLib.cpp synthesisLib.h
	$(CC) -c synthesisLib.cpp

# Removes all object and executable files
clean:
	rm -f *.o run