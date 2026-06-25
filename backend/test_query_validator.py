from query_validator import QueryValidator
validator = QueryValidator()
print(validator.validate("SELECT * FROM customers"))
print(validator.validate("DROP TABLE customers"))