from flask import Blueprint, request, jsonify

suggestions_bp = Blueprint('suggestions', __name__)

@suggestions_bp.route('', methods=['POST'])
def get_suggestions():
    # Get request data
    data = request.get_json()
    
    # Extract parameters
    trip_type = data.get('trip_type', '').lower()
    destination = data.get('destination', '').lower()
    duration_days = int(data.get('duration_days', 0))
    group_size = int(data.get('group_size', 1))
    
    # Initialize suggestions list
    suggestions = []
    
    # Trip type based suggestions
    if trip_type == 'trek':
        suggestions.extend([
            {"title": "Tent", "reason": "Essential for overnight stays during trek"},
            {"title": "Torch", "reason": "Necessary for visibility in dark conditions"},
            {"title": "First Aid Kit", "reason": "Safety precaution for outdoor activities"},
            {"title": "Energy Bars", "reason": "Quick nutrition during physical activity"},
            {"title": "Water Bottle", "reason": "Hydration is crucial during trekking"},
            {"title": "Hiking Boots", "reason": "Proper footwear for rough terrain"}
        ])
    elif trip_type == 'business trip':
        suggestions.extend([
            {"title": "Laptop", "reason": "Essential for work and presentations"},
            {"title": "Formal Wear", "reason": "Professional attire for meetings"},
            {"title": "ID Cards", "reason": "Required for identification and access"},
            {"title": "Business Cards", "reason": "Useful for networking"},
            {"title": "Chargers", "reason": "Keep your devices powered"}
        ])
    elif trip_type == 'college fest':
        suggestions.extend([
            {"title": "Banners", "reason": "Visual promotion for events"},
            {"title": "Laptops", "reason": "For presentations and managing events"},
            {"title": "Extension Cords", "reason": "Power supply for multiple devices"},
            {"title": "Costumes", "reason": "For performances or themed events"},
            {"title": "Portable Speakers", "reason": "For music and announcements"}
        ])
    elif trip_type == 'hackathon':
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
    
    if any(loc in destination for loc in rainy_destinations):
        suggestions.extend([
            {"title": "Raincoat", "reason": "Rainy weather at destination"},
            {"title": "Umbrella", "reason": "Protection from rain"},
            {"title": "Waterproof Bag Cover", "reason": "Keep belongings dry"}
        ])
    
    if any(loc in destination for loc in cold_destinations):
        suggestions.extend([
            {"title": "Warm Jacket", "reason": "Cold weather at destination"},
            {"title": "Gloves", "reason": "Protection for hands in cold weather"},
            {"title": "Thermal Wear", "reason": "Layer clothing for cold climate"}
        ])
    
    if any(loc in destination for loc in hot_destinations):
        suggestions.extend([
            {"title": "Sunscreen", "reason": "Protection from sun exposure"},
            {"title": "Hat", "reason": "Shield from direct sunlight"},
            {"title": "Sunglasses", "reason": "Eye protection in bright conditions"}
        ])
    
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
    
    return jsonify({"suggestions": suggestions}) 