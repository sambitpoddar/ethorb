import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ethorb",
    version="0.0.9",
    author="Sambit Poddar",
    author_email="sambitpoddar@yahoo.com",
    description="A powerful Python tool-kit for seamless interaction with Ethereum blockchain networks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sambitpoddar/ethorb",
    project_urls={
        "Bug Tracker": "https://github.com/sambitpoddar/ethorb/issues",
        "Documentation": "https://github.com/sambitpoddar/ethorb/blob/main/docs/readme.md",
        "Source Code": "https://github.com/sambitpoddar/ethorb/blob/main/ethorb/ethorb.py",
    },
    license="Apache License 2.0",
    packages=setuptools.find_packages(),
    package_data={'': ['README.md', 'LICENSE.txt']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        " :: Software Development :: Libraries",
    ],
    python_requires=">=3.6",
    install_requires=[
        "web3",
        "eth-utils",
        "eth-account",
        "requests",
        "setuptools>=50.0.0,<51.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0,<7.0.0",
            "black>=21.0b1,<22.0",
        ],
    },
    
    keywords="python package ethorb ethereum blockchain smart-contracts transaction",
)
