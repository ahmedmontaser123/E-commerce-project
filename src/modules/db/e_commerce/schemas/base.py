from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# this make srue that all the tables are created in the same database and can be easily imported in other modules without circular imports issues.
# make the sqlalchemy know that the class is a table in the data base 