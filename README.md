# Quick start

    # Install mongo server and python pip
    sudo apt-get install python-pip mongodb
    
    # Install required python libraries
    sudo pip install -r requirements.txt
    
    # Import photos
    python ./bin/import_media.py -d /path/to/media
    
    # Run server
    python ./bin/start_server.py

    # Open up http://localhost:5000/static/sample.html in browser :)
