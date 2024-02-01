import csv
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_script_for_sid(sid):
    driver = webdriver.Firefox()

    try:
        # Navigate to the website
        driver.get("https://builder.rcc-acis.org")

        # Find input elements by ID
        sid_input = driver.find_element(By.ID, "sid")
        elems_input = driver.find_element(By.ID, "elems")
        sdate_input = driver.find_element(By.ID, "sdate")
        edate_input = driver.find_element(By.ID, "edate")

        # Fill in the input fields
        sid_input.clear()
        sid_input.send_keys(str(sid))
        elems_input.send_keys("4")
        sdate_input.send_keys("1875-01-01")
        edate_input.send_keys("1988-01-01")

        # Find and click the 'Submit' button
        submit_button = driver.find_element(By.XPATH, '//button[text()="Submit"]')
        submit_button.click()

        # Explicitly wait for the presence of JSON data
        json_div = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//pre[contains(text(), "{") and contains(text(), "}")]'))
        )

        # Extract JSON text from the div element
        json_text = json_div.text.strip()

        # Parse JSON
        json_data = json.loads(json_text)

        # Check for the presence of the "error" key
        if "error" in json_data and json_data["error"] == "no data available":
            print(f"Error for SID {sid}: No data available.")
        else:
            # Save JSON data to a file
            output_filename = f"output_{sid}.json"
            with open(output_filename, "w") as json_file:
                json.dump(json_data, json_file, indent=2)
            print(f"JSON data for SID {sid} found and saved to {output_filename}.")
    except Exception as e:
        print(f"Error for SID {sid}: {e}")
    finally:
        # Close the browser
        driver.quit()

# Read station IDs from CSV file
csv_file_path = 'stations_metadata_of_three_counties.csv'  # Update with your CSV file path
with open(csv_file_path, 'r') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)  # Skip header row if present
 station_ids = [str(row[2]) for row in reader]



# Run the script for each station ID
for sid in station_ids:
    run_script_for_sid(sid)

#run_script_for_sid("94815")