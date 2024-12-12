import datetime
from flask import Blueprint, request, jsonify
from geopy.distance import geodesic
from app.models import db, Point, Polygon
import json

main = Blueprint('main', __name__)

@main.route('/points', methods=['POST'])
def create_point():
    data = request.get_json()
    point = Point(
        name=data['name'],
        description=data.get('description'),
        location=f"POINT({data['longitude']} {data['latitude']})"
    )
    db.session.add(point)
    db.session.commit()
    return jsonify({"message": "Point created successfully", "id": point.id}), 201

@main.route('/points', methods=['GET'])
def get_points():
    points = Point.query.all()
    result = [
        {
            "id": point.id,
            "name": point.name,
            "description": point.description,
            "location": {
                "latitude": point.location.coords[1],
                "longitude": point.location.coords[0]
            },
            "created_at": point.created_at
        }
        for point in points
    ]
    return jsonify(result)

@main.route('/polygons', methods=['POST'])
def create_polygon():
    data = request.get_json()
    coordinates = ", ".join([f"{lon} {lat}" for lat, lon in data['coordinates']])
    polygon = Polygon(
        name=data['name'],
        description=data.get('description'),
        boundary=f"POLYGON(({coordinates}))"  
    )
    db.session.add(polygon)
    db.session.commit()
    return jsonify({"message": "Polygon created successfully", "id": polygon.id}), 201

@main.route('/polygons', methods=['GET'])
def get_polygons():
    polygons = Polygon.query.all()
    result = [
        {
            "id": polygon.id,
            "name": polygon.name,
            "description": polygon.description,
            "boundary": [
                {"latitude": lat, "longitude": lon}
                for lon, lat in polygon.boundary.coords[0]
            ],
            "created_at": polygon.created_at
        }
        for polygon in polygons
    ]
    return jsonify(result)

@main.route('/data/points', methods=['POST'])
def create_point():
    data = request.get_json()
    point = Point(
        name=data['name'],
        description=data.get('description', ''),
        latitude=data['latitude'],
        longitude=data['longitude'],
        timestamp=datetime.utcnow()
    )
    db.session.add(point)
    db.session.commit()
    return jsonify({'objectId': point.id, 'message': 'Point created successfully!'})

@main.route('/data/points/<int:id>', methods=['GET'])
def get_point(id):
    point = Point.query.get_or_404(id)
    return jsonify({
        'objectId': point.id,
        'name': point.name,
        'description': point.description,
        'latitude': point.latitude,
        'longitude': point.longitude,
        'timestamp': point.timestamp.isoformat()
    })

@main.route('/data/points/<int:id>', methods=['PUT'])
def update_point(id):
    data = request.get_json()
    point = Point.query.get_or_404(id)

    point.name = data.get('name', point.name)
    point.description = data.get('description', point.description)
    point.latitude = data.get('latitude', point.latitude)
    point.longitude = data.get('longitude', point.longitude)
    
    
@main.route('/data/points', methods=['GET'])
def get_all_points():
    center_lat = request.args.get('latitude', type=float)
    center_lon = request.args.get('longitude', type=float)
    radius = request.args.get('radius', type=float)

    if center_lat is not None and center_lon is not None and radius is not None:
        center = (center_lat, center_lon)
        points = Point.query.all()

        result = []
        for point in points:
            distance = geodesic((point.latitude, point.longitude), center).meters
            if distance <= radius:
                result.append({
                    'objectId': point.id,
                    'name': point.name,
                    'description': point.description,
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'timestamp': point.timestamp.isoformat()
                })
        return jsonify(result)

    points = Point.query.all()
    result = [
        {
            'objectId': point.id,
            'name': point.name,
            'description': point.description,
            'latitude': point.latitude,
            'longitude': point.longitude,
            'timestamp': point.timestamp.isoformat()
        } for point in points
    ]
    return jsonify(result)

@main.route('/data/polygons', methods=['POST'])
def create_polygon():
    data = request.get_json()
    polygon = Polygon(
        name=data['name'],
        description=data.get('description', ''),
        coordinates=json.dumps(data['coordinates'])
    )
    db.session.add(polygon)
    db.session.commit()
    return jsonify({'objectId': polygon.id, 'message': 'Polygon created successfully!'})

@main.route('/data/polygons/<int:id>', methods=['GET'])
def get_polygon(id):
    polygon = Polygon.query.get_or_404(id)
    return jsonify({
        'objectId': polygon.id,
        'name': polygon.name,
        'description': polygon.description,
        'coordinates': json.loads(polygon.coordinates)
    })

@main.route('/data/polygons/<int:id>', methods=['PUT'])
def update_polygon(id):
    data = request.get_json()
    polygon = Polygon.query.get_or_404(id)

    polygon.name = data.get('name', polygon.name)
    polygon.description = data.get('description', polygon.description)
    polygon.coordinates = json.dumps(data.get('coordinates', json.loads(polygon.coordinates)))

    db.session.commit()
    return jsonify({'message': 'Polygon updated successfully!'})

@main.route('/data/polygons', methods=['GET'])
def get_all_polygons():
    polygons = Polygon.query.all()
    result = [
        {
            'objectId': polygon.id,
            'name': polygon.name,
            'description': polygon.description,
            'coordinates': json.loads(polygon.coordinates)
        } for polygon in polygons
    ]
    return jsonify(result)

