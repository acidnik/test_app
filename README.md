Run app
-------

```
docker-compose build
docker-compose up
```

App will be available at http://localhost:8000

Tests
-----

```
docker-compose run api pytest
```

Test data
---------
edit app/db.py (sample_data)
