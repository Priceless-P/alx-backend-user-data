
# Personal Data Protection Tasks

Solutions for tasks related to protecting personal data in a Python application.

## Tasks

### [0. Regex-ing](filtered_logger.py)

#### Requirements:
Write a function called `filter_datum` that returns the log message obfuscated.

**Arguments:**
- `fields`: a list of strings representing all fields to obfuscate
- `redaction`: a string representing by what the field will be obfuscated
- `message`: a string representing the log line
- `separator`: a string representing by which character is separating all fields in the log line (message)

The function should use a regex to replace occurrences of certain field values. `filter_datum` should be less than 5 lines long and use `re.sub` to perform the substitution with a single regex.

### [1. Log Formatter](filtered_logger.py)

#### Requirements:
Update the `RedactingFormatter` class to accept a list of strings `fields` constructor argument.

- Implement the `format` method to filter values in incoming log records using `filter_datum`. Values for fields in `fields` should be filtered.

**Tips:**
- The format method should be less than 5 lines long.

### [2. Create Logger](filtered_logger.py)

#### Requirements:
Implement a `get_logger` function that takes no arguments and returns a `logging.Logger` object.

- The logger should be named "user_data" and only log up to `logging.INFO` level. It should not propagate messages to other loggers. It should have a `StreamHandler` with `RedactingFormatter` as formatter.

- Create a tuple `PII_FIELDS` constant at the root of the module containing the fields from `user_data.csv` that are considered PII.

### [3. Connect to Secure Database](filtered_logger.py)

#### Requirements:
Implement a `get_db` function that returns a connector to the database (`mysql.connector.connection.MySQLConnection` object).

- Use the `os` module to obtain credentials from the environment and `mysql-connector-python` to connect to the MySQL database.

### [4. Read and Filter Data](filtered_logger.py)

#### Requirements:
Implement a `main` function that takes no arguments and returns nothing.

- The function will obtain a database connection using `get_db` and retrieve all rows in the `users` table. It should display each row under a filtered format as specified.

### [5. Encrypting Passwords](encrypt_password.py)

#### Requirements:
Implement a `hash_password` function that expects one string argument `password` and returns a salted, hashed password, which is a byte string.

- Use the `bcrypt` package to perform the hashing (with `hashpw`).

### [6. Check Valid Password](encrypt_password.py)

#### Requirements:
Implement an `is_valid` function that expects 2 arguments and returns a boolean.

**Arguments:**
- `hashed_password`: bytes type
- `password`: string type

Use `bcrypt` to validate that the provided password matches the hashed password.
