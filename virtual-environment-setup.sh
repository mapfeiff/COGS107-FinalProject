if [ "$OSTYPE" == "msys" ]
then
    #here for windows stuff
    #Create a virtual environment in the current directory
    python -m venv PythonVirtualEnvironment
    #activate the virtual environment
    ./PythonVirtualEnvironment/Scripts/activate

elif [ "$OSTYPE" == "darwin"* ]
then
    #here for macOS
    #Create a virtual environment in the current directory
    python -m venv PythonVirtualEnvironment
    #activate the virtual environment
    source ./PythonVirtualEnvironment/Scripts/activate

elif [ "$OSTYPE" == "linux"* ]
then
    #here for linux stuff
    #Create a virtual environment in the current directory
    python -m venv PythonVirtualEnvironment
    #activate the virtual environment
    source ./PythonVirtualEnvironment/Scripts/activate
fi