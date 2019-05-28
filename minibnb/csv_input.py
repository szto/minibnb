import csv
import mysql.connector
import my_settings

from django.db import connection


db_settings = my_settings.DATABASES
options = db_settings['default'].get('OPTIONS', None)

if options and 'read_default_file' in options:
    db = mysql.connector.connect(read_default_file=options['read_default_file'])
else:
    db_default = db_settings['default']
    db = mysql.connector.connect(host= db_default.get('HOST'),
                         user= db_default.get('USER'),
                         passwd= db_default.get('PASSWORD'),
                         db= db_default.get('NAME'))

cursor = db.cursor()
# cursor.execute(f"DELETE FROM heart_time")
# cursor.execute(f"DELETE FROM clothes")
# cursor.execute(f"DELETE FROM clothes_icon")
# cursor.execute(f"DELETE FROM temp_icon")

with open('city.csv') as csv_files:
    reader = csv.DictReader(csv_files)

    for row in reader:
        print(",".join(row))
        
        sql = f"""INSERT INTO cities (
            state_id,
            name
        ) VALUES (
            %(state_id)s,
            %(name)s
        )"""

        cursor.execute(sql, row)

db.commit()
db.close()