"""
Copyright 2020 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# dictionary for different granularity of TOP data intent
granular_intent = {
        "high":{
            "COMBINE": "combine",
            "GET_CONTACT": "get_contact",
            "GET_DIRECTIONS": "navigation",
            "GET_DISTANCE": "distance",
            "GET_ESTIMATED_ARRIVAL": "navigation",
            "GET_ESTIMATED_DEPARTURE": "navigation",
            "GET_ESTIMATED_DURATION": "navigation",
            "GET_EVENT": "get_event",
            "GET_EVENT_ATTENDEE": "get_event",
            "GET_EVENT_ATTENDEE_AMOUNT": "get_event",
            "GET_EVENT_ORGANIZER": "get_event",
            "GET_INFO_ROAD_CONDITION": "navigation",
            "GET_INFO_ROUTE": "navigation",
            "GET_INFO_TRAFFIC": "navigation",
            "GET_LOCATION": "get_location",
            "GET_LOCATION_HOME": "get_location",
            "GET_LOCATION_HOMETOWN": "get_location",
            "GET_LOCATION_SCHOOL": "get_location",
            "GET_LOCATION_WORK": "get_location",
            "NEGATION": "unsupported",
            "UNINTELLIGIBLE": "unsupported",
            "UNSUPPORTED": "unsupported",
            "UNSUPPORTED_EVENT": "unsupported",
            "UNSUPPORTED_NAVIGATION": "unsupported",
            "UPDATE_DIRECTIONS": "navigation"
            },
        "low":{
            "COMBINE": "combine",
            "GET_CONTACT": "get_contact",
            "GET_DIRECTIONS": "get_directions",
            "GET_DISTANCE": "get_distance",
            "GET_ESTIMATED_ARRIVAL": "get_time_estimate",
            "GET_ESTIMATED_DEPARTURE": "get_time_estimate",
            "GET_ESTIMATED_DURATION": "get_time_estimate",
            "GET_EVENT": "get_event",
            "GET_EVENT_ATTENDEE": "get_event",
            "GET_EVENT_ATTENDEE_AMOUNT": "get_event",
            "GET_EVENT_ORGANIZER": "get_event",
            "GET_INFO_ROAD_CONDITION": "get_road_info",
            "GET_INFO_ROUTE": "get_road_info",
            "GET_INFO_TRAFFIC": "get_road_info",
            "GET_LOCATION": "get_location",
            "GET_LOCATION_HOME": "get_location",
            "GET_LOCATION_HOMETOWN": "get_location",
            "GET_LOCATION_SCHOOL": "get_location",
            "GET_LOCATION_WORK": "get_location",
            "NEGATION": "unsupported",
            "UNINTELLIGIBLE": "unsupported",
            "UNSUPPORTED": "unsupported",
            "UNSUPPORTED_EVENT": "unsupported",
            "UNSUPPORTED_NAVIGATION": "unsupported",
            "UPDATE_DIRECTIONS": "update_directions"
            },
        "original":{
            "COMBINE": "combine",
            "GET_CONTACT": "get_contact",
            "GET_DIRECTIONS": "get_directions",
            "GET_DISTANCE": "get_distance",
            "GET_ESTIMATED_ARRIVAL": "get_estimated_arrival",
            "GET_ESTIMATED_DEPARTURE": "get_estimated_departure",
            "GET_ESTIMATED_DURATION": "get_estimated_duration",
            "GET_EVENT": "get_event",
            "GET_EVENT_ATTENDEE": "get_event_attendee",
            "GET_EVENT_ATTENDEE_AMOUNT": "get_event_attendee_amount",
            "GET_EVENT_ORGANIZER": "get_event_organizer",
            "GET_INFO_ROAD_CONDITION": "get_info_road_condition",
            "GET_INFO_ROUTE": "get_info_route",
            "GET_INFO_TRAFFIC": "get_info_traffic",
            "GET_LOCATION": "get_location",
            "GET_LOCATION_HOME": "get_location_home",
            "GET_LOCATION_HOMETOWN": "get_location_hometown",
            "GET_LOCATION_SCHOOL": "get_location_school",
            "GET_LOCATION_WORK": "get_location_work",
            "NEGATION": "negation",
            "UNINTELLIGIBLE": "unintelligible",
            "UNSUPPORTED": "unsupported",
            "UNSUPPORTED_EVENT": "unsupported_event",
            "UNSUPPORTED_NAVIGATION": "unsupported_navigation",
            "UPDATE_DIRECTIONS": "update_directions"
            }
}
