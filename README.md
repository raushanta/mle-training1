1. create a src folder and inside that create a folder ```mle_training1_raushanta``` and inside this folder paste all the python files.
2. ```__init__.py``` file is also required make a empty file.
3. Build the distribution folder and run the command ```python -m build```.
4. Upload the distribution archives by running command ```python -m twine upload --repository testpypi dist/*```.
5. Install the package by running the command ```py -m pip install --index-url https://test.pypi.org/simple/ --no-deps mle_training1_raushanta```
6. Now you are ready to use your own library.