# Project with a Graph Database (Neo4j)

This project is a implementation of a CRUD  using `neo4j`.

## Getting Started

### Prerequisistes

* Python
* Neo4j
* Node
* React

### Installing

1. Clone this repository:

``` bash
git clone git@github.com:JuanDiazuwu/db_neo4j_project.git
```

2. Create a virtual enviroment(recommended), you can change the second `venv` by the name that you want:

```
    python -m venv venv
```

3. Activate the virtual env:

* On Windows:

```
    venv\Scripts\activate
```

* On macOS and Linux:

```
    . ./bin/activate
```

4. Install the required dependencies:

```
    pip install -r requirements.txt
```

5. To run the backend:

```
cd backend
```

``` bash
uvicorn app:app --reload
```

6. You can open a browser and navigate to `http://127.0.0.1:8000/docs` to view backend's docs.

7. To run frontend:

```
cd client
```

8. Install node dependencies:

```
npm install
```

9. Run app:

``` bash
npm run dev
```

10. Open a browser and navigate to `http://127.0.0.1:5173` to the web.

### Run with docker backend

1. Move to backend:

``` bash
cd backend
```

2. Build backend image:

``` bash
docker build -t neo4j_fastapi_app .
```

3. To run the backend:

``` bash
docker run -d -p 8000:8000 --name crud_neo4j neo4j_fastapi_app
```

### Run with docker frontend
<!--to do-->

### Run all with docker-compose

1. Need to be at the root of the project.

2. Run docker-compose.yml:

``` bash
docker-compose up -d
```

## Authors

:blue_heart: **Cristian Loera** - [CrisRLoera](https://github.com/CrisRLoera)

:blue_heart: **Juan Díaz** - [Fuan200](https://github.com/Fuan200)