import argparse

from homecontrol.api.database.client import APIDatabaseClient


parser = argparse.ArgumentParser(
    prog="init_db", description="Initialises the homecontrol database"
)

print("Initialising the homecontrol database...")
database_client = APIDatabaseClient()
with database_client.connect() as conn:
    conn.init_db()
print("Done!")
