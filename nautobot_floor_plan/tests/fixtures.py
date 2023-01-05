"""Fixtures for testing this app."""

from django.contrib.contenttypes.models import ContentType

from nautobot.dcim.models import Location, LocationType, Site
from nautobot.extras.models import Status

from nautobot_floor_plan.models import FloorPlan, FloorPlanTile


def create_prerequisites(floor_count=3):
    """Fixture to create the various prerequisite objects needed before a FloorPlan can be created."""
    parent_location_type = LocationType.objects.create(name="Building")
    location_type = LocationType.objects.create(name="Floor", parent=parent_location_type)

    active_status = Status.objects.get(name="Active")
    active_status.content_types.add(ContentType.objects.get_for_model(FloorPlanTile))

    site = Site.objects.create(name="Site 1", status=active_status)
    building = Location.objects.create(
        site=site, location_type=parent_location_type, name="Building 1", status=active_status
    )
    floors = []
    for i in range(1, floor_count + 1):
        floors.append(
            Location.objects.create(
                location_type=location_type, parent=building, status=active_status, name=f"Floor {i}"
            )
        )

    return {
        "status": active_status,
        "floors": floors,
    }


def create_floor_plans(locations):
    """Fixture to create necessary number of FloorPlan for tests."""
    size = 1
    floor_plans = []

    for location in locations:
        floor_plan = FloorPlan(location=location, x_size=size, y_size=size)
        floor_plan.validated_save()
        floor_plans.append(floor_plan)
        size += 1

    return floor_plans
