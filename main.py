import os
from flask import Flask, request, jsonify
from transformers import pipeline
import pudb
app = Flask(__name__)

# Load the text classification pipeline
classifier = pipeline("image-classification", model="Kaludi/food-category-classification-v2.0")

category_details_dict = {
    "Bread": {
      "pros": ["Provides energy due to its carbohydrate content.", "Versatile ingredient used in various cuisines and dishes."],
      "cons": ["Some types of bread, especially white bread, may be low in fiber and nutrients.", "Overconsumption of certain bread types may contribute to weight gain."],
      "allergens": ["Gluten (wheat)"]
    },
    "Dairy": {
      "pros": ["Excellent source of calcium for bone health.", "Provides protein and essential vitamins."],
      "cons": ["Some individuals may be lactose intolerant, causing digestive issues.", "High-fat dairy products can contribute to elevated cholesterol levels if consumed excessively."],
      "allergens": ["Lactose", "Casein"]
    },
    "Dessert": {
      "pros": ["Offers enjoyment and satisfaction, especially after a meal.", "Can provide a source of comfort and celebration in social settings."],
      "cons": ["Often high in sugar and calories, leading to weight gain and potential health issues.", "Excessive consumption may contribute to dental problems and blood sugar spikes."],
      "allergens": ["Milk", "Eggs", "Nuts"]
    },
    "Egg": {
      "pros": ["High-quality protein source with essential nutrients.", "Versatile ingredient used in a wide range of dishes."],
      "cons": ["High in cholesterol, which may be a concern for individuals with certain health conditions.", "Allergic reactions to eggs are relatively common, particularly in children."],
      "allergens": ["Eggs"]
    },
    "Fried Food": {
      "pros": ["Offers crispy texture and rich flavor.", "Can be a satisfying indulgence on occasion."],
      "cons": ["High in unhealthy fats and calories, contributing to obesity and heart disease.", "Consuming fried foods regularly may increase the risk of developing chronic health conditions."],
      "allergens": ["Gluten (if breaded)"]
    },
    "Fruit": {
      "pros": ["Rich in vitamins, minerals, and antioxidants.", "Provides natural sweetness and hydration."],
      "cons": ["Some fruits are high in natural sugars, which can be a concern for individuals monitoring their sugar intake.", "Excessive consumption of acidic fruits may contribute to dental erosion."],
      "allergens": ["None"]
    },
    "Meat": {
      "pros": ["Excellent source of high-quality protein and essential nutrients like iron and zinc.", "Provides satiety and helps build and repair tissues in the body."],
      "cons": ["High consumption of red and processed meats has been linked to an increased risk of certain diseases, such as cardiovascular disease and cancer.", "Environmental concerns related to meat production, including greenhouse gas emissions and land use."],
      "allergens": ["None"]
    },
    "Noodles": {
      "pros": ["Quick and convenient meal option, especially for busy lifestyles.", "Can be a source of complex carbohydrates and some essential nutrients."],
      "cons": ["Many commercially available noodles are highly processed and may lack nutritional value.", "Consuming noodles frequently, particularly with high-calorie sauces, can contribute to weight gain and blood sugar imbalances."],
      "allergens": ["Gluten (wheat)"]
    },
    "Rice": {
      "pros": ["Staple food in many cultures, providing a source of energy and sustenance.", "Can be a gluten-free alternative for those with gluten sensitivities."],
      "cons": ["Some types of rice, especially white rice, are low in fiber and nutrients compared to whole grains.", "Consuming large portions of rice regularly may contribute to spikes in blood sugar levels and insulin resistance."],
      "allergens": ["None"]
    },
    "Seafood": {
      "pros": ["Rich in omega-3 fatty acids, which are beneficial for heart and brain health.", "Provides high-quality protein and essential nutrients like vitamin D and selenium."],
      "cons": ["Concerns about mercury contamination in certain types of seafood, particularly larger predatory fish.", "Environmental sustainability issues related to overfishing and habitat destruction."],
      "allergens": ["Fish", "Shellfish"]
    },
    "Soup": {
      "pros": ["Hydrating and comforting, especially during cold weather or when feeling unwell.", "Can be a nutritious way to incorporate vegetables, proteins, and grains into the diet."],
      "cons": ["Some commercially prepared soups may be high in sodium and additives.", "Low-calorie soups may not provide sufficient satiety for some individuals if consumed as a main meal."],
      "allergens": ["None"]
    },
    "Vegetable": {
      "pros": ["Rich in vitamins, minerals, and antioxidants, supporting overall health and immunity.", "Low in calories and high in fiber, promoting digestive health and weight management."],
      "cons": ["Some vegetables may contain naturally occurring compounds that can cause digestive discomfort in sensitive individuals (e.g., cruciferous vegetables like broccoli and cabbage).", "Pesticide residues may be a concern for conventionally grown vegetables, prompting some consumers to opt for organic varieties."],
      "allergens": ["None"]
    }
}


@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']

    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file:
        file.save(os.path.join("./images/", file.filename))
        return jsonify({"message": "File uploaded successfully", "filename": file.filename}), 200
    else:
        return jsonify({"message": "File format not supported"}), 400

# curl -X POST -H "Content-Type: application/json" -d '{"image": "base64_encoded_image_string_here"}'

@app.route('/classify', methods=['GET'])
def classify_text():
    # Get the text to classify from the request query parameters
    text = request.args.get('text', '')

    # Perform sentiment analysis on the provided text
    model_output = classifier(text)
    label = model_output[0]['label']
    # Return the classification result
    return_value = category_details_dict[label].copy()
    return_value.update(model_output[0])
    return return_value


if __name__ == '__main__':
    app.run(debug=True)
