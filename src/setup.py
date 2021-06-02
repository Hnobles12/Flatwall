
from setuptools import setup, find_packages

setup(
    name="flatwall",
    version='1.0.0',
    packages=find_packages('flatwall'),
    install_requires=['opencv-python', 'click', 'numpy'],
    entry_points={
        'console_scripts':[
            'flatwall = flatwall:main'
        ]
    },
    python_requires='>=3.8',
    

)
