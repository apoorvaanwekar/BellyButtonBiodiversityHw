# Import Dependencies
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import os 

# Create engine using the `hawaii.sqlite` database file
engine = create_engine('sqlite:///Data/belly_button_biodiversity.sqlite')

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# assign otu table to variable
OTU = Base.classes.otu

# assign samples table to variable
Sample = Base.classes.samples

# assign samples_metadata table to variable
Sample_Meta = Base.classes.samples_metadata

# Create a session
session = Session(engine)
