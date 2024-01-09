from bs4 import BeautifulSoup
import requests
import pandas as pd

df = pd.DataFrame(columns = ["Vehicle Name", "Price", "Body Type","Transmission","Drive Type","Engine","Fuel Type","Location","Odometer (KMs)", "Link to Listing"])

def init(user_input_url):
    url = user_input_url

    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')

    car_table = soup.find_all('table', class_='info-details-list')
    car_titles = soup.find_all('div', itemprop='name description')
    car_prices = soup.find_all('span', itemprop="price")
    car_offer_prices = soup.find_all('span', itemprop='offers')

    car_url = soup.find_all('a', itemprop='url')

    i = 0

    for car in car_table:
        vehicle_title = car_titles[i].text.strip()

        if i < len(car_prices):
            vehicle_price = f'${car_prices[i].text.strip()}'

        elif i > len(car_prices) & i < len(car_offer_prices):

            vehicle_price = car_offer_prices[i].text.strip()

        vehicle_type = car.find_all('td')[1].text.strip()
        vehicle_transmission =  car.find_all('td')[3].text.strip()
        vehicle_drive_type =  car.find_all('td')[5].text.strip()
        vehicle_engine =  car.find_all('td')[7].text.strip()
        vehicle_fuel_type =  car.find_all('td')[9].text.strip()
        vehicle_location =  car.find_all('td')[11].text.strip()
        vehicle_odometer =  car.find_all('td')[13].text.strip()

        vehicle_url = []
        for url in car_url:
            if i < len(car_url):
                vehicle_url.append(f'www.turners.co.nz{url.get('href',None)}')

        individual_car_data = [vehicle_title, vehicle_price,  vehicle_type, vehicle_transmission, vehicle_drive_type, vehicle_engine, vehicle_fuel_type, vehicle_location, vehicle_odometer, vehicle_url[i]]
        
        length = len(df)
        df.loc[length] = individual_car_data
        i += 1
    df.to_csv("list.csv", index=False)
    print(f"Successfully compiled a list of cars for sale!")

print("This is the initiate function, used to initiate the scraping script. Change this url (making sure it uses turners.co.nz/Cars/Used-Cars-for-Sale/ as a base)\nFor e.g. the url would be 'turners.co.nz/Cars/Used-Cars-for-Sale/'\nYou can use the filters on the website to narrow down the results.")
website = input("Please enter a 'turners.co.nz/Cars/Used-Cars-for-Sale/' link >> ")
init(website)