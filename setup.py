from setuptools import setup, find_packages

# Lee el contenido del README.md para la descripción larga
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="BKLibDB",  # Nombre del paquete
    version="0.3.0",  # Versión incrementada para reflejar las nuevas funcionalidades
    author="Elieser Castro",
    author_email="bkelidireccion@gmail.com",
    description=(
        "Una librería que utiliza SQLAlchemy y otras dependencias "
        "para generar managers y models que permiten consultar bases de datos SQL y NoSQL."
    ),
    long_description=long_description,  # Descripción larga desde README.md
    long_description_content_type="text/markdown",
    url="https://github.com/theleerise/BKLibDB.git",
    license="Personal Use Only",
    classifiers=[
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries",
    ],
    packages=find_packages(),  # Encuentra todos los subpaquetes automáticamente
    python_requires=">=3.10",  # Versión mínima de Python
    install_requires=[
        "greenlet>=3.1.1",           # Soporte para SQLAlchemy
        "psycopg2>=2.9.10",          # PostgreSQL
        "pyodbc>=5.2.0",             # SQL Server
        "oracledb>=3.1.0",           # Oracle database
        "SQLAlchemy>=2.0.36",        # ORM para bases de datos relacionales
        "pymongo>=4.6.0",            # MongoDB
        "cassandra-driver>=3.25.0",  # Cassandra
        "redis>=5.0.1",              # Redis
        "neo4j>=5.17.0",             # Neo4j
        "typing_extensions>=4.12.2", # Extensiones de tipado
    ],
    include_package_data=True,  # Incluye archivos adicionales en MANIFEST.in
    project_urls={
        "Source": "https://github.com/theleerise/BKLibDB.git",
        "Bug Tracker": "https://github.com/theleerise/BKLibDB/issues",
    },
)
