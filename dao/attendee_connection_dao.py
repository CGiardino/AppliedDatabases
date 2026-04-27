from typing import Any

from utils.db_utils import create_neo4j_driver
from exceptions.attendee_exceptions import AttendeesAlreadyConnectedError


def fetch_connected_attendees_in_graph(attendee_id: int) -> list[dict[str, Any]]:
	query = (
		"MATCH (a:Attendee {AttendeeID: $attendee_id})-[:CONNECTED_TO]-(connected:Attendee) "
		"WHERE connected.AttendeeID <> $attendee_id "
		"RETURN DISTINCT connected.AttendeeID AS attendeeID "
		"ORDER BY attendeeID"
	)

	def fetch_tx(tx, param_attendee_id):
		result = tx.run(query, attendee_id=param_attendee_id)
		return [record.data() for record in result]

	driver = create_neo4j_driver()
	try:
		with driver.session() as session:
			return session.execute_read(fetch_tx, attendee_id)
	finally:
		driver.close()

def add_attendee_relationship_in_graph(attendee_id: int, connected_attendee_id: int) -> None:
	check_query = (
		"MATCH (a1:Attendee {AttendeeID: $attendee_id})-[:CONNECTED_TO]-(a2:Attendee {AttendeeID: $connected_attendee_id}) "
		"RETURN COUNT(*) AS rel_count"
	)
	create_query = (
		"MATCH (a1:Attendee {AttendeeID: $attendee_id}), (a2:Attendee {AttendeeID: $connected_attendee_id}) "
		"MERGE (a1)-[:CONNECTED_TO]-(a2)"
	)

	def add_relationship_tx(tx, param_attendee_id, param_connected_attendee_id):
		result = tx.run(check_query, attendee_id=param_attendee_id, connected_attendee_id=param_connected_attendee_id)
		rel_count = result.single()["rel_count"]
		if rel_count > 0:
			raise AttendeesAlreadyConnectedError("Attendees are already connected.")
		tx.run(create_query, attendee_id=param_attendee_id, connected_attendee_id=param_connected_attendee_id)

	driver = create_neo4j_driver()
	try:
		with driver.session() as session:
			session.execute_write(add_relationship_tx, attendee_id, connected_attendee_id)
	finally:
		driver.close()

def add_attendee_in_graph(attendee_id: int) -> None:
	query = (
		"MERGE (a:Attendee {AttendeeID: $attendee_id}) "
		"RETURN a"
	)

	def add_attendee_tx(tx, param_attendee_id):
		tx.run(query, attendee_id=param_attendee_id)

	driver = create_neo4j_driver()
	try:
		with driver.session() as session:
			session.execute_write(add_attendee_tx, attendee_id)
	finally:
		driver.close()
	
def attendee_exists_in_graph(attendee_id: int) -> bool:
	query = (
		"MATCH (a:Attendee {AttendeeID: $attendee_id}) "
		"RETURN COUNT(a) > 0 AS attendee_exists"
	)

	def exists_tx(tx, param_attendee_id):
		result = tx.run(query, attendee_id=param_attendee_id)
		record = result.single()
		return bool(record and record["attendee_exists"])

	driver = create_neo4j_driver()
	try:
		with driver.session() as session:
			return session.execute_read(exists_tx, attendee_id)
	finally:
		driver.close()

# Delete attendee and all their relationships
def delete_attendee_in_graph(attendee_id: int) -> None:
	query = (
		"MATCH (a:Attendee {AttendeeID: $attendee_id}) "
		#detach delete removes the node and all its relationships
		"DETACH DELETE a"
	)

	def delete_tx(tx, param_attendee_id):
		tx.run(query, attendee_id=param_attendee_id)

	driver = create_neo4j_driver()
	try:
		with driver.session() as session:
			session.execute_write(delete_tx, attendee_id)
	finally:
		driver.close()

