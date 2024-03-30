# Prerequisites

Before running the code, make sure you have the following installed:

- Python 3
- Virtualenv

To install Virtualenv, run the following command:
```
python3 -m pip install virtualenv
```

# Run

To execute the code using the virtual environment (venv), follow these steps:

1. Create a virtual environment named `myenv` by running the following command:
    ```
    python3 -m venv myenv
    ```

2. Activate the virtual environment by running the appropriate command based on your operating system:
    - For Linux/Mac:
        ```
        source myenv/bin/activate
        ```
    - For Windows:
        ```
        myenv\Scripts\activate
        ```

3. Install the required packages by running the following command:
    ```
    pip install -r requirements.txt
    ```

4. Once the virtual environment is activated and the requirements are installed, you can run your Python code using the `python` command:
    ```
    python ./main.py
    ```

5. Remember to deactivate the virtual environment when you're done by running the following command:
    ```
    deactivate
    ```
