# Amazon DocumentDB Tools

Steps to migrate indexes from Mongo to DocumentDB:
1. Run python3.8 install if it's not available `./install-python.sh`
2. Run dump script `./dump_index.sh <mongo_password>`
3. Run restore script `./restore_index.sh <mongo_password> <documentDB host>`
