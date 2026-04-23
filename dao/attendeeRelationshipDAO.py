from typing import Any

from config.db_config import NEO4J_CONFIG
from utils.db_utils import create_neo4j_driver
from exceptions.attendee_exceptions import AttendeesAlreadyConnectedError


def fetch_connected_attendees(attendee_id: int) -> list[dict[str, Any]]:
	query = (
		'MATCH (a:Attendee {AttendeeID: $attendee_id})-[:CONNECTED_TO]-(connected:Attendee) '
		'WHERE connected.AttendeeID <> $attendee_id '
		'RETURN DISTINCT connected.AttendeeID AS attendeeID '
		'ORDER BY attendeeID'
	)

	driver = create_neo4j_driver()
	try:
		with driver.session(database=NEO4J_CONFIG['database']) as session:
			result = session.run(query, attendee_id=attendee_id)
			return [record.data() for record in result]
	finally:
		driver.close()

def add_attendee_relationship(attendee_id: int, connected_attendee_id: int) -> None:
	check_query = (
		'MATCH (a1:Attendee {AttendeeID: $attendee_id})-[:CONNECTED_TO]-(a2:Attendee {AttendeeID: $connected_attendee_id}) '
		'RETURN COUNT(*) AS rel_count'
	)
	create_query = (
		'MATCH (a1:Attendee {AttendeeID: $attendee_id}), (a2:Attendee {AttendeeID: $connected_attendee_id}) '
		'MERGE (a1)-[:CONNECTED_TO]-(a2)'
	)

	driver = create_neo4j_driver()
	try:
		with driver.session(database=NEO4J_CONFIG['database']) as session:
			result = session.run(check_query, attendee_id=attendee_id, connected_attendee_id=connected_attendee_id)
			rel_count = result.single()['rel_count']
			if rel_count > 0:
				raise AttendeesAlreadyConnectedError("Attendees are already connected.")
			session.run(create_query, attendee_id=attendee_id, connected_attendee_id=connected_attendee_id)
	finally:
		driver.close()

def add_attendee_in_graph(attendee_id: int) -> None:
	query = (
		'MERGE (a:Attendee {AttendeeID: $attendee_id}) '
		'RETURN a'
	)
	driver = create_neo4j_driver()
	try:
		with driver.session(database=NEO4J_CONFIG['database']) as session:
			session.run(query, attendee_id=attendee_id)
	finally:
		driver.close()
	
def attendee_exists_in_graph(attendee_id: int) -> bool:
	query = (
		'MATCH (a:Attendee {AttendeeID: $attendee_id}) '
		'RETURN COUNT(a) > 0 AS attendee_exists'
	)

	driver = create_neo4j_driver()
	try:
		with driver.session(database=NEO4J_CONFIG['database']) as session:
			result = session.run(query, attendee_id=attendee_id)
			record = result.single()
			return bool(record and record['attendee_exists'])
	finally:
		driver.close()
