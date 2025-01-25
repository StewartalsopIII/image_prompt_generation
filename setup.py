from setuptools import setup, find_packages

setup(
    name="image_generation",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'replicate==0.20.0',
        'python-dotenv==1.0.0',
        'Pillow==10.2.0',
        'requests==2.31.0',
    ],
)