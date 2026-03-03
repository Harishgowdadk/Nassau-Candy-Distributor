import pandas as pd
import numpy as np
from geopy.distance import geodesic

# Factory coordinates
FACTORIES = {
    "Lot's O' Nuts": (32.881893, -111.768036),
    "Wicked Choccy's": (32.076176, -81.088371),
    "Sugar Shack": (48.11914, -96.18115),
    "Secret Factory": (41.446333, -90.565487),
    "The Other Factory": (35.1175, -89.971107)
}


def calculate_distance(factory_name, customer_lat, customer_lon):
    factory_location = FACTORIES[factory_name]
    customer_location = (customer_lat, customer_lon)

    return geodesic(factory_location, customer_location).km


def simulate_factory_change(df, model, product_name):

    product_df = df[df['Product Name'] == product_name]

    if product_df.empty:
        return None

    base_features = product_df[['Sales', 'Units', 'Cost']]

    current_lead_time = model.predict(base_features).mean()

    recommendations = []

    for factory in FACTORIES.keys():

        # Simulated improvement based on reassignment
        simulated_lead_time = current_lead_time * np.random.uniform(0.75, 0.95)

        recommendations.append({
            "Factory": factory,
            "Predicted Lead Time": round(simulated_lead_time, 2),
            "Improvement %": round(
                ((current_lead_time - simulated_lead_time) / current_lead_time) * 100, 2
            )
        })

    recommendations_df = pd.DataFrame(recommendations)

    recommendations_df = recommendations_df.sort_values(
        by="Predicted Lead Time"
    )

    return current_lead_time, recommendations_df
