### Setup
1. Install python 3.7
2. Install requirements
    `pip install -r requirements.txt`

3. Environment Variable
    - `DATABASE_URL` - Postgres Database URL

4. Feed data in Postgres
    ```
    python geofeed.py # inserting geodata.json file into postgres
    python mapping_feed.py # inserting pincode location data into postgres
    ```

5. Start application
    - Using uvicorn, for local development mainly
        ```
        uvicorn main:app --reload
        ```
    
    - Using Unicorn server, for staging or production level deployment
        ```
        gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
        ```




### Data
**NOTE** : Input data files are in `data` folder, inside root dir. If you want to choose data files from another path, you have to edit the code, no CLI options provided


### Docs
1. Postman collection is provided in `docs` folder
2. Code level commenting and documentation is done in code file itself