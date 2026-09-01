import pandas as pd
import numpy as np
import requests
import logging

# Configure logging to see what the script is doing
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_cneos_data():
    """Fetches raw close-approach data directly from NASA CNEOS API."""
    logging.info("Fetching raw data from NASA CNEOS API...")
    url = "https://ssd-api.jpl.nasa.gov/cad.api"
    params = {
        'dist-max': '0.05',  # Within 0.05 Astronomical Units (~19.5 Lunar Distances)
        'fullname': 'true',
        'date-min': '2000-01-01',
        'sort': 'dist'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    json_data = response.json()
    
    fields = json_data['fields']
    records = json_data['data']
    df = pd.DataFrame(records, columns=fields)
    logging.info(f"Successfully downloaded {len(df)} records from NASA.")
    return df


def transform_data(df):
    """Cleans data, performs unit conversions, and calculates risk scores."""
    logging.info("Cleaning data and calculating risk metrics...")
    
    # 1. Rename columns to standardized names
    column_mapping = {
        'des': 'object_designation',
        'cd': 'close_approach_date',
        'dist': 'miss_distance_au',
        'v_rel': 'velocity_km_s',
        'h': 'absolute_magnitude_h'
    }
    df = df.rename(columns=column_mapping)
    
    # 2. Convert data types
    df['object_designation'] = df['object_designation'].astype(str).str.strip()
    df['close_approach_date'] = pd.to_datetime(df['close_approach_date'])
    df['miss_distance_au'] = pd.to_numeric(df['miss_distance_au'], errors='coerce')
    df['velocity_km_s'] = pd.to_numeric(df['velocity_km_s'], errors='coerce')
    df['absolute_magnitude_h'] = pd.to_numeric(df['absolute_magnitude_h'], errors='coerce')
    
    # Remove rows missing essential info
    df = df.dropna(subset=['miss_distance_au', 'velocity_km_s', 'absolute_magnitude_h'])
    
    # 3. Astronomical Conversions
    # 1 AU = 149,597,870.7 km | 1 AU = 389.6 Lunar Distances (LD)
    df['miss_distance_km'] = (df['miss_distance_au'] * 149597870.7).round(2)
    df['miss_distance_ld'] = (df['miss_distance_au'] * 389.6).round(2)
    
    # 4. Estimate Asteroid Diameter in Meters (using average albedo = 0.14)
    df['est_diameter_m'] = (
        (1329 / np.sqrt(0.14)) * (10 ** (-0.2 * df['absolute_magnitude_h'])) * 1000
    ).round(2)
    
    # 5. Categorize by Size
    size_bins = [-np.inf, 30, 140, 1000, np.inf]
    size_labels = [
        'Small (<30m)', 
        'Medium (30-140m)', 
        'Potentially Hazardous Size (140m-1km)', 
        'Planet-Threat (>1km)'
    ]
    df['size_class'] = pd.cut(df['est_diameter_m'], bins=size_bins, labels=size_labels)
    
    # 6. Calculate Risk Score (0 to 100 Scale)
    dist_factor = np.clip((10 - df['miss_distance_ld']) / 10, 0, 1) * 45
    size_factor = np.clip(df['est_diameter_m'] / 500, 0, 1) * 35
    vel_factor = np.clip(df['velocity_km_s'] / 40, 0, 1) * 20
    
    df['risk_score'] = (dist_factor + size_factor + vel_factor).round(2)
    
    # 7. Assign Risk Tiers
    risk_bins = [-np.inf, 40, 70, np.inf]
    risk_labels = ['Low Threat', 'Moderate Risk', 'High Priority']
    df['risk_level'] = pd.cut(df['risk_score'], bins=risk_bins, labels=risk_labels)
    
    logging.info("Data cleaning and scoring finished.")
    return df


def load_data(df, output_filename='nasa_cneos_cleaned.csv'):
    """Saves the final clean dataset to a CSV file."""
    df.to_csv(output_filename, index=False)
    logging.info(f"Saved cleaned data file as: {output_filename}")


if __name__ == "__main__":
    # Execute the steps
    raw_data = extract_cneos_data()
    clean_data = transform_data(raw_data)
    load_data(clean_data)
    print("\nSUCCESS! Here is a preview of your cleaned data:\n")
    print(clean_data[['object_designation', 'close_approach_date', 'est_diameter_m', 'risk_score', 'risk_level']].head())