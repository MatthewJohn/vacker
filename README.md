# NOTE

This repo is a mirror of phabricator DockStudios. Do not make any changes outside of this.

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

# Working with front-end app

    npm start
      Starts the development server.
    
    npm run build
      Bundles the app into static files for production.
    
    npm test
      Starts the test runner.
    
    npm run eject
      Removes this tool and copies build dependencies, configuration files
      and scripts into the app directory. If you do this, you can’t go back!

