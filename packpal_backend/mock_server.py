from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Persistence file paths
DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db')
os.makedirs(DB_DIR, exist_ok=True)
USERS_FILE = os.path.join(DB_DIR, 'users.json')
CHECKLISTS_FILE = os.path.join(DB_DIR, 'checklists.json')
ITEMS_FILE = os.path.join(DB_DIR, 'items.json')

# Initialize mock database 
def load_db():
    mock_db = {
        "users": {},
        "checklists": {},
        "checklist_items": {}
    }
    
    # Load users if file exists
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                mock_db["users"] = json.load(f)
        except:
            print("Error loading users file")
    
    # Load checklists if file exists
    if os.path.exists(CHECKLISTS_FILE):
        try:
            with open(CHECKLISTS_FILE, 'r') as f:
                mock_db["checklists"] = json.load(f)
        except:
            print("Error loading checklists file")
    
    # Load items if file exists
    if os.path.exists(ITEMS_FILE):
        try:
            with open(ITEMS_FILE, 'r') as f:
                mock_db["checklist_items"] = json.load(f)
        except:
            print("Error loading items file")
    
    return mock_db

# Save database to files
def save_db(mock_db):
    # Save users
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(mock_db["users"], f)
    except:
        print("Error saving users file")
    
    # Save checklists
    try:
        with open(CHECKLISTS_FILE, 'w') as f:
            json.dump(mock_db["checklists"], f)
    except:
        print("Error saving checklists file")
    
    # Save items
    try:
        with open(ITEMS_FILE, 'w') as f:
            json.dump(mock_db["checklist_items"], f)
    except:
        print("Error saving items file")

# Load the database
mock_db = load_db()

@app.route('/api/suggestions', methods=['POST', 'OPTIONS'])
def get_suggestions():
    """Handle suggestions requests"""
    # Handle preflight request
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response
        
    # Get and print request data
    data = request.get_json()
    print("="*50)
    print("RECEIVED SUGGESTION REQUEST")
    print("="*50)
    print(f"Trip type: {data.get('trip_type', '')}")
    print(f"Destination: {data.get('destination', '')}")
    print(f"Duration days: {data.get('duration_days', 0)}")
    print(f"Group size: {data.get('group_size', 1)}")
    print("="*50)
    
    # Extract parameters
    trip_type = data.get('trip_type', '').lower()
    destination = data.get('destination', '').lower()
    duration_days = int(data.get('duration_days', 0))
    group_size = int(data.get('group_size', 1))
    
    # Initialize suggestions list
    suggestions = []
    
    # Trip type based suggestions
    if 'trek' in trip_type:
        suggestions.extend([
            {"title": "Tent", "reason": "Essential for overnight stays during trek"},
            {"title": "Torch", "reason": "Necessary for visibility in dark conditions"},
            {"title": "First Aid Kit", "reason": "Safety precaution for outdoor activities"},
            {"title": "Energy Bars", "reason": "Quick nutrition during physical activity"},
            {"title": "Water Bottle", "reason": "Hydration is crucial during trekking"},
            {"title": "Hiking Boots", "reason": "Proper footwear for rough terrain"}
        ])
    elif 'business' in trip_type:
        suggestions.extend([
            {"title": "Laptop", "reason": "Essential for work and presentations"},
            {"title": "Formal Wear", "reason": "Professional attire for meetings"},
            {"title": "ID Cards", "reason": "Required for identification and access"},
            {"title": "Business Cards", "reason": "Useful for networking"},
            {"title": "Chargers", "reason": "Keep your devices powered"}
        ])
    elif 'college' in trip_type or 'fest' in trip_type:
        suggestions.extend([
            {"title": "Banners", "reason": "Visual promotion for events"},
            {"title": "Laptops", "reason": "For presentations and managing events"},
            {"title": "Extension Cords", "reason": "Power supply for multiple devices"},
            {"title": "Costumes", "reason": "For performances or themed events"},
            {"title": "Portable Speakers", "reason": "For music and announcements"}
        ])
    elif 'hack' in trip_type:
        suggestions.extend([
            {"title": "Laptop", "reason": "Essential for coding and development"},
            {"title": "Chargers", "reason": "Keep your devices powered"},
            {"title": "Power Bank", "reason": "Backup power for mobile devices"},
            {"title": "Headphones", "reason": "For focus and concentration"},
            {"title": "Notebook", "reason": "For sketching ideas and taking notes"}
        ])
    
    # Weather-based suggestions - simulated weather check
    rainy_destinations = ['seattle', 'london', 'mumbai', 'vancouver', 'kerala']
    cold_destinations = ['alaska', 'helsinki', 'toronto', 'moscow', 'oslo']
    hot_destinations = ['dubai', 'cairo', 'phoenix', 'las vegas', 'chennai']
    
    for loc in rainy_destinations:
        if loc in destination:
            suggestions.extend([
                {"title": "Raincoat", "reason": "Rainy weather at destination"},
                {"title": "Umbrella", "reason": "Protection from rain"},
                {"title": "Waterproof Bag Cover", "reason": "Keep belongings dry"}
            ])
            break
    
    for loc in cold_destinations:
        if loc in destination:
            suggestions.extend([
                {"title": "Warm Jacket", "reason": "Cold weather at destination"},
                {"title": "Gloves", "reason": "Protection for hands in cold weather"},
                {"title": "Thermal Wear", "reason": "Layer clothing for cold climate"}
            ])
            break
    
    for loc in hot_destinations:
        if loc in destination:
            suggestions.extend([
                {"title": "Sunscreen", "reason": "Protection from sun exposure"},
                {"title": "Hat", "reason": "Shield from direct sunlight"},
                {"title": "Sunglasses", "reason": "Eye protection in bright conditions"}
            ])
            break
    
    # Duration-based suggestions
    if duration_days > 7:
        suggestions.extend([
            {"title": "Laundry Bag", "reason": "Extended stay requires laundry management"},
            {"title": "Travel Detergent", "reason": "For washing clothes on longer trips"}
        ])
    
    # Group size based suggestions
    if group_size > 5:
        suggestions.extend([
            {"title": "Group First Aid Kit", "reason": "Larger group needs more medical supplies"},
            {"title": "Megaphone", "reason": "Communication in larger groups"}
        ])

    print(f"Returning {len(suggestions)} suggestions")
    
    # Create response with CORS headers
    response = jsonify({"suggestions": suggestions})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    """Handle login requests"""
    # Handle preflight request
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response
    
    # Process login request
    data = request.get_json()
    email = data.get('email', '')
    password = data.get('password', '')
    
    print("="*50)
    print("LOGIN ATTEMPT")
    print("="*50)
    print(f"Email: {email}")
    print(f"Password: {password}")
    print("="*50)
    
    # Check if user exists and password matches
    if email in mock_db["users"] and mock_db["users"][email]["password"] == password:
        user = mock_db["users"][email]
        print(f"Login successful for {email}")
        response = jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": email
            },
            "token": "mock-auth-token-12345"
        })
    else:
        if email not in mock_db["users"]:
            print(f"Login failed: User {email} not found")
        else:
            print(f"Login failed: Password incorrect for {email}")
            
        response = jsonify({
            "success": False,
            "message": "Invalid email or password"
        })
    
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/auth/signup', methods=['POST', 'OPTIONS'])
def signup():
    """Handle signup requests"""
    # Handle preflight request
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response
    
    # Process signup request
    data = request.get_json()
    name = data.get('name', '')
    email = data.get('email', '')
    password = data.get('password', '')
    
    print("="*50)
    print("SIGNUP ATTEMPT")
    print("="*50)
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Password: {password}")
    print("="*50)
    
    # Check if user already exists
    if email in mock_db["users"]:
        print(f"Signup failed: Email {email} already exists")
        response = jsonify({
            "success": False,
            "message": "User with this email already exists"
        })
    else:
        # Save user to mock database
        user_id = len(mock_db["users"]) + 1
        mock_db["users"][email] = {
            "id": user_id,
            "name": name,
            "email": email,
            "password": password
        }
        print(f"Signup successful: Created user {email}")
        print(f"User database now has {len(mock_db['users'])} users")
        
        # Mock successful signup response
        response = jsonify({
            "success": True,
            "message": "Signup successful",
            "user": {
                "id": user_id,
                "name": name,
                "email": email
            },
            "token": "mock-auth-token-12345"
        })
    
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/checklists', methods=['GET', 'POST', 'OPTIONS'])
def checklists():
    """Handle checklists requests"""
    # Handle preflight request
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        return response
    
    if request.method == 'GET':
        # Return all checklists
        checklists_list = list(mock_db["checklists"].values())
        response = jsonify({"checklists": checklists_list})
    else:  # POST
        # Create new checklist
        data = request.get_json()
        checklist_id = len(mock_db["checklists"]) + 1
        checklist = {
            "id": checklist_id,
            "title": data.get('title', 'New Checklist'),
            "description": data.get('description', ''),
            "creator_id": data.get('creator_id', 1)
        }
        mock_db["checklists"][checklist_id] = checklist
        response = jsonify({"success": True, "checklist": checklist})
    
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/checklist-items/<item_id>', methods=['PUT', 'DELETE', 'OPTIONS'])
def manage_checklist_item(item_id):
    """Handle update and delete checklist item requests"""
    global mock_db
    
    # Reload DB to ensure it's current
    mock_db = load_db()
    
    # Handle preflight request
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'PUT,DELETE,OPTIONS')
        return response
    
    # Handle DELETE
    if request.method == 'DELETE':
        print("="*50)
        print(f"DELETING CHECKLIST ITEM: {item_id}")
        print("="*50)
        
        # Convert ID to both string and integer for lookup
        str_id = str(item_id)
        int_id = int(item_id) if str_id.isdigit() else None
        
        # Show current items
        print(f"Current items in DB: {list(mock_db['checklist_items'].keys())}")
        
        # Check all possible ID formats
        found = False
        for key in [str_id, int_id]:
            if key is not None and key in mock_db["checklist_items"]:
                del mock_db["checklist_items"][key]
                print(f"Successfully deleted item {item_id} (key: {key})")
                found = True
                break
        
        if not found:
            print(f"Item {item_id} not found, but returning success anyway")
        
        # Save updated DB
        save_db(mock_db)
        
        # Return success response with proper CORS headers
        result = {"success": True, "message": f"Item {item_id} deleted successfully"}
        response = jsonify(result)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Content-Type', 'application/json')
        return response
    
    # Handle PUT (update)
    elif request.method == 'PUT':
        print("="*50)
        print(f"UPDATING CHECKLIST ITEM: {item_id}")
        print("="*50)
        
        # Get request data
        data = request.get_json()
        print(f"Update data: {data}")
        
        # Convert ID to both string and integer for lookup
        str_id = str(item_id)
        int_id = int(item_id) if str_id.isdigit() else None
        
        # Show current items
        print(f"Current items in DB: {list(mock_db['checklist_items'].keys())}")
        
        # Check all possible ID formats
        found = False
        for key in [str_id, int_id]:
            if key is not None and key in mock_db["checklist_items"]:
                # Update fields
                if 'title' in data:
                    mock_db["checklist_items"][key]["title"] = data["title"]
                if 'status' in data:
                    mock_db["checklist_items"][key]["status"] = data["status"]
                
                updated_item = mock_db["checklist_items"][key]
                print(f"Successfully updated item {item_id} (key: {key}): {updated_item}")
                found = True
                
                # Save updated DB
                save_db(mock_db)
                
                result = {"success": True, "message": f"Item {item_id} updated successfully", "item": updated_item}
                response = jsonify(result)
                response.headers.add('Access-Control-Allow-Origin', '*')
                response.headers.add('Content-Type', 'application/json')
                return response
        
        # If we get here, item was not found
        print(f"Item {item_id} not found")
        result = {"success": False, "message": f"Item {item_id} not found"}
        response = jsonify(result)
        response.status_code = 404
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Content-Type', 'application/json')
        return response

@app.route('/api/checklist-items', methods=['POST', 'OPTIONS'])
def create_checklist_item():
    """Handle create checklist item requests"""
    global mock_db
    
    # Reload DB to ensure it's current
    mock_db = load_db()
    
    # Handle preflight request
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response
    
    # Process create request
    data = request.get_json()
    print("="*50)
    print("CREATING CHECKLIST ITEM")
    print("="*50)
    print(f"Title: {data.get('title', 'New Item')}")
    print(f"Status: {data.get('status', 'To Pack')}")
    print(f"Checklist ID: {data.get('checklist_id', 1)}")
    print("="*50)
    
    # Generate a new item ID - ensure it's unique among both string and int keys
    existing_ids = set()
    for key in mock_db["checklist_items"].keys():
        try:
            if isinstance(key, str) and key.isdigit():
                existing_ids.add(int(key))
            elif isinstance(key, int):
                existing_ids.add(key)
        except:
            pass
    
    item_id = 1
    while item_id in existing_ids:
        item_id += 1
    
    # Create the new item
    item = {
        "id": item_id,
        "title": data.get('title', 'New Item'),
        "checklist_id": data.get('checklist_id', 1),
        "status": data.get('status', 'To Pack'),
        "completed": False
    }
    
    # Store in DB as BOTH string and integer key for maximum compatibility
    mock_db["checklist_items"][item_id] = item
    mock_db["checklist_items"][str(item_id)] = item
    
    print(f"Created new item with ID: {item_id} and status: {item['status']}")
    print(f"Current items in DB: {list(mock_db['checklist_items'].keys())}")
    
    # Save updated DB
    save_db(mock_db)
    
    response = jsonify({"success": True, "item": item})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Mock server is running. Use /api/suggestions to get suggestions."})

if __name__ == '__main__':
    print("Starting mock server on http://localhost:8000")
    print("To test: curl -X POST http://localhost:8000/api/suggestions -H 'Content-Type: application/json' -d '{\"trip_type\": \"Trek\", \"destination\": \"Seattle\", \"duration_days\": 5, \"group_size\": 4}'")
    app.run(debug=True, port=8000, host='0.0.0.0') 