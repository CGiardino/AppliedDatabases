from typing import Any

from config.db_config import NEO4J_CONFIG
from utils.db_utils import create_neo4j_driver


def fetch_connected_attendees(attendee_id: int) -> list[dict[str, Any]]:
	query = (
		'MATCH (a:Attendee {AttendeeID: $attendee_id}) '
		'OPTIONAL MATCH (a)-[:CONNECTED_TO]-(connected:Attendee) '
		'WITH DISTINCT connected.AttendeeID AS connected_attendee_id '
		'WHERE connected_attendee_id IS NOT NULL AND connected_attendee_id <> $attendee_id '
		'RETURN connected_attendee_id AS attendeeID '
		'ORDER BY attendeeID'
	)

	driver = create_neo4j_driver()
	try:
		with driver.session(database=NEO4J_CONFIG['database']) as session:
			result = session.run(query, attendee_id=attendee_id)
			return [record.data() for record in result]
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



