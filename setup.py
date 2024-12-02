from setuptools import setup, find_packages

# Lee el contenido del README.md para la descripción larga
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="BKLibDB",  # Nombre del paquete
    version="0.1.0",  # Versión inicial
    author="Elieser Castro",
    author_email="bkelidireccion@gmail.com",
    description=(
        "Una librería que utiliza SQLAlchemy, pyodbc y otras dependencias "
        "para generar manager y models con los cuales consultar bases de datos."
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
    ],
    packages=find_packages(),  # Encuentra todos los subpaquetes automáticamente
    python_requires=">=3.11",  # Versión mínima de Python
    install_requires=[
        "greenlet>=3.1.1",
        "psycopg2>=2.9.10",
        "pyodbc>=5.2.0",
        "SQLAlchemy>=2.0.36",
        "typing_extensions>=4.12.2",
    ],
    include_package_data=True,  # Incluye archivos adicionales en MANIFEST.in
)
