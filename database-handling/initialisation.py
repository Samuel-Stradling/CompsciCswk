import sqlite3


def init_all():
    # creates database if doesn't exist
    conn = sqlite3.connect("data\main.sql")
    try:
        cursor = conn.cursor()

        # Create Companies
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Companies (
                ticker TEXT PRIMARY KEY,
                name TEXT,
                sector TEXT,
                description TEXT,
                incorporation_year INTEGER
            )
        """
        )

        # Create Date Statuses
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS DateStatuses (
                date DATE PRIMARY KEY,
                complete_data BOOLEAN,
                market_open BOOLEAN
            )
        """
        )

        # Create Stock Prices
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS StockPrices (
                priceid INTEGER PRIMARY KEY,
                ticker TEXT,
                date DATE,
                open REAL,
                close REAL,
                high REAL,
                volume INTEGER,
                weighted_volume REAL,
                FOREIGN KEY (ticker) REFERENCES Companies (ticker),
                FOREIGN KEY (date) REFERENCES DateStatuses (date)
            )
        """
        )

        conn.commit()

    except sqlite3.Error as error:
        print("Error: {}".format(error))
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def fill_Companies_table():
    # hard coded 🤷‍♂️🤢
    company_dictionary = {
    'MSFT': ['Microsoft Corporation', 'Technology', 'A multinational technology company known for its software products.', 1975],
    'AAPL': ['Apple Inc.', 'Technology', 'A technology company that designs and manufactures consumer electronics and software.', 1976],
    'NVDA': ['NVIDIA Corporation', 'Technology', 'A technology company that designs graphics processing units (GPUs) for gaming and professional markets.', 1993],
    'AMZN': ['Amazon.com Inc.', 'Retail', 'An e-commerce and cloud computing company.', 1994],
    'TSLA': ['Tesla Inc.', 'Automotive', 'An electric vehicle and clean energy company.', 2003],
    'META': ['Meta Platforms Inc. (formerly Facebook)', 'Technology', 'A social media and technology conglomerate.', 2004],
    'GOOGL': ['Alphabet Inc. (Google Class A)', 'Technology', 'A multinational technology company focusing on internet-related services.', 1998],
    'GOOG': ['Alphabet Inc. (Google Class C)', 'Technology', 'A multinational technology company focusing on internet-related services.', 1998],
    'AVGO': ['Broadcom Inc.', 'Technology', 'A semiconductor company.', 1961],
    'PEP': ['PepsiCo Inc.', 'Beverages', 'A multinational food and beverage company.', 1965],
    'COST': ['Costco Wholesale Corporation', 'Retail', 'A multinational corporation operating a chain of membership-only warehouse clubs.', 1976],
    'ADBE': ['Adobe Inc.', 'Technology', 'A multinational software company.', 1982],
    'CSCO': ['Cisco Systems Inc.', 'Technology', 'A multinational technology conglomerate.', 1984],
    'NFLX': ['Netflix Inc.', 'Entertainment', 'A streaming service and content production company.', 1997],
    'AMD': ['Advanced Micro Devices Inc.', 'Technology', 'A semiconductor company that produces computer processors and related technologies.', 1969],
    'CMCSA': ['Comcast Corporation', 'Telecommunication', 'A telecommunications conglomerate providing cable television and internet services.', 1963],
    'TMUS': ['T-Mobile US Inc.', 'Telecommunication', 'A telecommunications company providing wireless services.', 1990],
    'TXN': ['Texas Instruments Inc.', 'Technology', 'A semiconductor company specializing in integrated circuits.', 1930],
    'HON': ['Honeywell International Inc.', 'Technology', 'A conglomerate company operating in multiple industries.', 1906],
    'INTC': ['Intel Corporation', 'Technology', 'A multinational semiconductor company.', 1968],
    'QCOM': ['QUALCOMM Incorporated', 'Technology', 'A multinational semiconductor and telecommunications equipment company.', 1985],
    'INTU': ['Intuit Inc.', 'Technology', 'A financial software company.', 1983],
    'AMGN': ['Amgen Inc.', 'Healthcare', 'A multinational biotechnology company.', 1980],
    'AMAT': ['Applied Materials Inc.', 'Technology', 'A semiconductor equipment company.', 1967],
    'ISRG': ['Intuitive Surgical Inc.', 'Medical Devices', 'A medical technology company.', 1995],
    'SBUX': ['Starbucks Corporation', 'Food and Beverage', 'A multinational chain of coffeehouses.', 1971],
    'MDLZ': ['Mondelez International Inc.', 'Food and Beverage', 'A multinational confectionery, food, and beverage company.', 2012],
    'BKNG': ['Booking Holdings Inc.', 'Technology', 'An online travel agency.', 1997],
    'GILD': ['Gilead Sciences Inc.', 'Healthcare', 'A biopharmaceutical company.', 1987],
    'ADI': ['Analog Devices Inc.', 'Technology', 'A semiconductor company specializing in data conversion and signal processing technology.', 1965],
    'ADP': ['Automatic Data Processing Inc.', 'Technology', 'A human resources management software and services provider.', 1949],
    'VRTX': ['Vertex Pharmaceuticals Incorporated', 'Healthcare', 'A biotechnology company.', 1989],
    'LRCX': ['Lam Research Corporation', 'Technology', 'A semiconductor equipment company.', 1980],
    'PANW': ['Palo Alto Networks Inc.', 'Technology', 'A cybersecurity company.', 2005],
    'REGN': ['Regeneron Pharmaceuticals Inc.', 'Healthcare', 'A biotechnology company.', 1988],
    'PYPL': ['PayPal Holdings Inc.', 'Financial Services', 'An online payments and financial services company.', 1998],
    'CSX': ['CSX Corporation', 'Transportation', 'A railroad transportation company.', 1980],
    'MU': ['Micron Technology Inc.', 'Technology', 'A multinational semiconductor memory company.', 1978],
    'SNPS': ['Synopsys Inc.', 'Technology', 'A semiconductor design company.', 1986],
    'ATVI': ['Activision Blizzard Inc.', 'Entertainment', 'A video game holding company.', 2008],
    'KLAC': ['KLA Corporation', 'Technology', 'A process control and yield management solutions company.', 1975],
    'CDNS': ['Cadence Design Systems Inc.', 'Technology', 'A multinational electronic design automation software and engineering services company.', 1988],
    'ASML': ['ASML Holding NV', 'Technology', 'A multinational company that produces photolithography equipment used in the semiconductor manufacturing process.', 1984],
    'MELI': ['MercadoLibre Inc.', 'E-commerce', 'A South American e-commerce and online payments company.', 1999],
    'MNST': ['Monster Beverage Corporation', 'Beverages', 'A beverage company specializing in energy drinks.', 1935],
    'FTNT': ['Fortinet Inc.', 'Technology', 'A multinational cybersecurity company.', 2000],
    'ORLY': ["O'Reilly Automotive Inc.", 'Automotive', 'A retailer of automotive parts, tools, supplies, equipment, and accessories.', 1957],
    'MAR': ['Marriott International Inc.', 'Hospitality', 'A multinational hospitality company.', 1927],
    'CHTR': ['Charter Communications Inc.', 'Telecommunication', 'A telecommunications company providing cable television, internet, and telephone services.', 1993],
    'ABNB': ['Airbnb Inc.', 'Hospitality', 'An online marketplace for lodging and tourism activities.', 2008],
    'NXPI': ['NXP Semiconductors NV', 'Technology', 'A semiconductor company.', 1953],
    'MRVL': ['Marvell Technology Group Ltd.', 'Technology', 'A semiconductor company.', 1995],
    'DXCM': ['DexCom Inc.', 'Medical Devices', 'A medical device company.', 1999],
    'CTAS': ['Cintas Corporation', 'Business Services', 'A business services company specializing in uniform rental services.', 1929],
    'MCHP': ['Microchip Technology Inc.', 'Technology', 'A semiconductor company.', 1989],
    'MRNA': ['Moderna Inc.', 'Healthcare', 'A biotechnology company.', 2010],
    'LULU': ['Lululemon Athletica Inc.', 'Apparel', 'A yoga-inspired athletic apparel company.', 1998],
    'WDAY': ['Workday Inc.', 'Technology', 'A multinational enterprise software company.', 2005],
    'KDP': ['Keurig Dr Pepper Inc.', 'Beverages', 'A multinational beverage conglomerate.', 2018],
    'AEP': ['American Electric Power Company Inc.', 'Utilities', 'A public utility holding company.', 1906],
    'KHC': ['The Kraft Heinz Company', 'Food and Beverage', 'A multinational food and beverage company.', 2015],
    'PDD': ['Pinduoduo Inc.', 'E-commerce', 'A Chinese e-commerce platform.', 2015],
    'ADSK': ['Autodesk Inc.', 'Technology', 'A multinational software corporation.', 1982],
    'CPRT': ['Copart Inc.', 'Automotive', 'An online vehicle auction company.', 1982],
    'PCAR': ['PACCAR Inc.', 'Automotive', 'A multinational truck manufacturing company.', 1905],
    'BIIB': ['Biogen Inc.', 'Healthcare', 'A multinational biotechnology company.', 1978],
    'EXC': ['Exelon Corporation', 'Utilities', 'A utility services holding company.', 2000],
    'IDXX': ['IDEXX Laboratories Inc.', 'Healthcare', 'A veterinary diagnostics and software company.', 1983],
    'PAYX': ['Paychex Inc.', 'Business Services', 'A provider of payroll, human resource, and benefits outsourcing services.', 1971],
    'ODFL': ['Old Dominion Freight Line Inc.', 'Transportation', 'A less-than-truckload shipping company.', 1934],
    'ON': ['ON Semiconductor Corporation', 'Technology', 'A semiconductor company.', 1999],
    'AZN': ['AstraZeneca PLC', 'Healthcare', 'A multinational pharmaceutical and biopharmaceutical company.', 1999],
    'ROST': ['Ross Stores Inc.', 'Retail', 'An American off-price department store chain.', 1982],
    'GEHC': ['General Electric Healthcare (GEHC)', 'Healthcare', 'A division of General Electric that focuses on healthcare.', 1892],
    'SGEN': ['Seagen Inc.', 'Healthcare', 'A biotechnology company.', 1997],
    'CSGP': ['CoStar Group Inc.', 'Technology', 'A provider of commercial real estate information and analytics.', 1987],
    'EA': ['Electronic Arts Inc.', 'Entertainment', 'A video game company.', 1982],
    'XEL': ['Xcel Energy Inc.', 'Utilities', 'A utility holding company.', 1909],
    'GFS': ['GrafTech International Ltd.', 'Manufacturing', 'A manufacturer of graphite electrodes.', 1886],
    'FAST': ['Fastenal Company', 'Manufacturing', 'A wholesaler and retailer of industrial and construction supplies.', 1967],
    'CTSH': ['Cognizant Technology Solutions Corporation', 'Technology', 'A multinational technology company providing IT services.', 1994],
    'VRSK': ['Verisk Analytics Inc.', 'Technology', 'A data analytics and risk assessment company.', 1971],
    'CRWD': ['CrowdStrike Holdings Inc.', 'Technology', 'A cybersecurity technology company.', 2011],
    'DLTR': ['Dollar Tree Inc.', 'Retail', 'An American chain of discount variety stores.', 1986],
    'BKR': ['Baker Hughes', 'Energy', 'An energy technology company.', 1907],
    'WBD': ['Weibo Corporation', 'Technology', 'A Chinese social media company.', 2009],
    'CEG': ['Constellation Energy Group Inc.', 'Utilities', 'A utility company.', 1906],
    'ILMN': ['Illumina Inc.', 'Healthcare', 'A biotechnology company.', 1998],
    'DDOG': ['Datadog Inc.', 'Technology', 'A monitoring and analytics platform for cloud-scale applications.', 2010],
    'ANSS': ['ANSYS Inc.', 'Technology', 'A simulation software company.', 1970],
    'TEAM': ['Atlassian Corporation Plc', 'Technology', 'A multinational software company.', 2002],
    'ALGN': ['Align Technology Inc.', 'Medical Devices', 'A medical device company specializing in clear aligners.', 1997],
    'WBA': ['Walgreens Boots Alliance Inc.', 'Retail', 'A holding company for a chain of pharmacies.', 1901],
    'EBAY': ['eBay Inc.', 'E-commerce', 'An online marketplace.', 1995],
    'FANG': ['Diamondback Energy Inc.', 'Energy', 'An independent oil and natural gas company.', 2007],
    'ENPH': ['Enphase Energy Inc.', 'Energy', 'A renewable energy technology company.', 2006],
    'ZS': ['Zscaler Inc.', 'Technology', 'A cloud security company.', 2008],
    'SIRI': ['Sirius XM Holdings Inc.', 'Telecommunication', 'A broadcasting company.', 1990],
    'ZM': ['Zoom Video Communications Inc.', 'Technology', 'A video conferencing software company.', 2011],
    'JD': ['JD.com Inc.', 'E-commerce', 'A Chinese e-commerce company.', 1998],
    'LCID': ['Lucid Group Inc.', 'Automotive', 'An electric vehicle manufacturer.', 2007]
    }

    try:
        conn = sqlite3.connect('data\main.sql')
        cursor = conn.cursor()

        # SQL query to insert data into the Companies table
        insert_query = "INSERT INTO Companies (ticker, name, sector, description, incorporation_year) VALUES (?, ?, ?, ?, ?)"

        # Loop through the dictionary and insert each company's information
        for ticker, company_info in company_dictionary.items():
            name, sector, description, incorporation_year = company_info
            data = (ticker, name, sector, description, incorporation_year)
            cursor.execute(insert_query, data)

        # Commit the changes to the database
        conn.commit()

        print("Data inserted successfully.")

    except sqlite3.Error as error:
        print("Error: {}".format(error))

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()





def add_historic_data():
    import sys
    sys.path.insert(1, 'C:\\Users\Sam\\Documents\\Programming\\CompsciCswk\\api\\')


    from dataHandling import call_all_companies 

    print(call_all_companies("2023-08-07"))


def fill_dates_for_historic_data():
    from datetime import datetime, timedelta

    # Get the current date
    current_date = datetime.now()

    # Calculate the date three years ago from the current date
    three_years_ago = current_date - timedelta(days=3*365)  # Approximate for simplicity

    # Iterate through the dates from three years ago until the current date
    date_iterator = three_years_ago
    while date_iterator <= current_date:
        print(date_iterator.date())  # Print the date portion
        date_iterator += timedelta(days=1)  # Move to the next day


add_historic_data()

# MAKE DATAHANDLING.PY INTO CLASS WITH TOOL METHODS???
