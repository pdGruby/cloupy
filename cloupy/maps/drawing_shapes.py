

def calc_the_distance(
        point1, point2
):
    """Calculate the distance between two given points"""
    import math

    a = abs(point1[0] - point2[0])
    b = abs(point1[1] - point2[1])
    c2 = a ** 2 + b ** 2

    c = math.sqrt(c2)

    return c


def get_countries_list_for_default_shape():
    return [('Zimbabwe', 'Zimbabwe', 'ZWE'), ('Zambia', 'Zambia', 'ZMB'), ('Yemen', 'Yemen', 'YEM'),
            ('Vietnam', 'Vietnam', 'VNM'), ('Venezuela', 'Venezuela', 'VEN'), ('Vatican', 'Vatican', 'VAT'),
            ('Vanuatu', 'Vanuatu', 'VUT'), ('Uzbekistan', 'Uzbekistan', 'UZB'), ('Uruguay', 'Uruguay', 'URY'),
            ('Federated States of Micronesia', 'Federated States of Micronesia', 'FSM'),
            ('Marshall Islands', 'Marshall Islands', 'MHL'),
            ('United States of America', 'Northern Mariana Islands', 'MNP'),
            ('United States of America', 'United States Virgin Islands', 'VIR'),
            ('United States of America', 'Guam', 'GUM'), ('United States of America', 'American Samoa', 'ASM'),
            ('United States of America', 'Puerto Rico', 'PRI'),
            ('United States of America', 'United States of America', 'USA'),
            ('United Kingdom', 'South Georgia and the Islands', 'SGS'),
            ('United Kingdom', 'British Indian Ocean Territory', 'IOT'),
            ('United Kingdom', 'Saint Helena', 'SHN'), ('United Kingdom', 'Pitcairn Islands', 'PCN'),
            ('United Kingdom', 'Anguilla', 'AIA'),
            ('United Kingdom', 'Falkland Islands', 'FLK'), ('United Kingdom', 'Cayman Islands', 'CYM'),
            ('United Kingdom', 'Bermuda', 'BMU'),
            ('United Kingdom', 'British Virgin Islands', 'VGB'), ('United Kingdom', 'Turks and Caicos Islands', 'TCA'),
            ('United Kingdom', 'Montserrat', 'MSR'), ('United Kingdom', 'Jersey', 'JEY'),
            ('United Kingdom', 'Guernsey', 'GGY'),
            ('United Kingdom', 'Isle of Man', 'IMN'), ('United Kingdom', 'United Kingdom', 'GBR'),
            ('United Arab Emirates', 'United Arab Emirates', 'ARE'), ('Ukraine', 'Ukraine', 'UKR'),
            ('Uganda', 'Uganda', 'UGA'),
            ('Turkmenistan', 'Turkmenistan', 'TKM'), ('Turkey', 'Turkey', 'TUR'), ('Tunisia', 'Tunisia', 'TUN'),
            ('Trinidad and Tobago', 'Trinidad and Tobago', 'TTO'), ('Tonga', 'Tonga', 'TON'), ('Togo', 'Togo', 'TGO'),
            ('East Timor', 'East Timor', 'TLS'), ('Thailand', 'Thailand', 'THA'),
            ('United Republic of Tanzania', 'United Republic of Tanzania', 'TZA'),
            ('Tajikistan', 'Tajikistan', 'TJK'), ('Taiwan', 'Taiwan', 'TWN'), ('Syria', 'Syria', 'SYR'),
            ('Switzerland', 'Switzerland', 'CHE'),
            ('Sweden', 'Sweden', 'SWE'), ('Swaziland', 'Swaziland', 'SWZ'), ('Suriname', 'Suriname', 'SUR'),
            ('South Sudan', 'South Sudan', 'SDS'), ('Sudan', 'Sudan', 'SDN'), ('Sri Lanka', 'Sri Lanka', 'LKA'),
            ('Spain', 'Spain', 'ESP'), ('South Korea', 'South Korea', 'KOR'), ('South Africa', 'South Africa', 'ZAF'),
            ('Somalia', 'Somalia', 'SOM'), ('Somaliland', 'Somaliland', 'SOL'),
            ('Solomon Islands', 'Solomon Islands', 'SLB'),
            ('Slovakia', 'Slovakia', 'SVK'), ('Slovenia', 'Slovenia', 'SVN'), ('Singapore', 'Singapore', 'SGP'),
            ('Sierra Leone', 'Sierra Leone', 'SLE'), ('Seychelles', 'Seychelles', 'SYC'),
            ('Republic of Serbia', 'Republic of Serbia', 'SRB'),
            ('Senegal', 'Senegal', 'SEN'), ('Saudi Arabia', 'Saudi Arabia', 'SAU'),
            ('São Tomé and Principe', 'São Tomé and Principe', 'STP'),
            ('San Marino', 'San Marino', 'SMR'), ('Samoa', 'Samoa', 'WSM'),
            ('Saint Vincent and the Grenadines', 'Saint Vincent and the Grenadines', 'VCT'),
            ('Saint Lucia', 'Saint Lucia', 'LCA'), ('Saint Kitts and Nevis', 'Saint Kitts and Nevis', 'KNA'),
            ('Rwanda', 'Rwanda', 'RWA'),
            ('Russia', 'Russia', 'RUS'), ('Romania', 'Romania', 'ROU'), ('Qatar', 'Qatar', 'QAT'),
            ('Portugal', 'Portugal', 'PRT'),
            ('Poland', 'Poland', 'POL'), ('Philippines', 'Philippines', 'PHL'), ('Peru', 'Peru', 'PER'),
            ('Paraguay', 'Paraguay', 'PRY'),
            ('Papua New Guinea', 'Papua New Guinea', 'PNG'), ('Panama', 'Panama', 'PAN'), ('Palau', 'Palau', 'PLW'),
            ('Pakistan', 'Pakistan', 'PAK'), ('Oman', 'Oman', 'OMN'), ('Norway', 'Norway', 'NOR'),
            ('North Korea', 'North Korea', 'PRK'),
            ('Nigeria', 'Nigeria', 'NGA'), ('Niger', 'Niger', 'NER'), ('Nicaragua', 'Nicaragua', 'NIC'),
            ('New Zealand', 'New Zealand', 'NZL'),
            ('New Zealand', 'Niue', 'NIU'), ('New Zealand', 'Cook Islands', 'COK'),
            ('Netherlands', 'Netherlands', 'NLD'),
            ('Netherlands', 'Aruba', 'ABW'), ('Netherlands', 'Curaçao', 'CUW'), ('Nepal', 'Nepal', 'NPL'),
            ('Nauru', 'Nauru', 'NRU'),
            ('Namibia', 'Namibia', 'NAM'), ('Mozambique', 'Mozambique', 'MOZ'), ('Morocco', 'Morocco', 'MAR'),
            ('Western Sahara', 'Western Sahara', 'SAH'),
            ('Montenegro', 'Montenegro', 'MNE'), ('Mongolia', 'Mongolia', 'MNG'), ('Moldova', 'Moldova', 'MDA'),
            ('Monaco', 'Monaco', 'MCO'),
            ('Mexico', 'Mexico', 'MEX'), ('Mauritius', 'Mauritius', 'MUS'), ('Mauritania', 'Mauritania', 'MRT'),
            ('Malta', 'Malta', 'MLT'),
            ('Mali', 'Mali', 'MLI'), ('Maldives', 'Maldives', 'MDV'), ('Malaysia', 'Malaysia', 'MYS'),
            ('Malawi', 'Malawi', 'MWI'),
            ('Madagascar', 'Madagascar', 'MDG'), ('North Macedonia', 'North Macedonia', 'MKD'),
            ('Luxembourg', 'Luxembourg', 'LUX'),
            ('Lithuania', 'Lithuania', 'LTU'), ('Liechtenstein', 'Liechtenstein', 'LIE'), ('Libya', 'Libya', 'LBY'),
            ('Liberia', 'Liberia', 'LBR'), ('Lesotho', 'Lesotho', 'LSO'), ('Lebanon', 'Lebanon', 'LBN'),
            ('Latvia', 'Latvia', 'LVA'),
            ('Laos', 'Laos', 'LAO'), ('Kyrgyzstan', 'Kyrgyzstan', 'KGZ'), ('Kuwait', 'Kuwait', 'KWT'),
            ('Kosovo', 'Kosovo', 'KOS'),
            ('Kiribati', 'Kiribati', 'KIR'), ('Kenya', 'Kenya', 'KEN'), ('Kazakhstan', 'Kazakhstan', 'KAZ'),
            ('Jordan', 'Jordan', 'JOR'),
            ('Japan', 'Japan', 'JPN'), ('Jamaica', 'Jamaica', 'JAM'), ('Italy', 'Italy', 'ITA'),
            ('Israel', 'Israel', 'ISR'),
            ('Israel', 'Palestine', 'PSX'), ('Ireland', 'Ireland', 'IRL'), ('Iraq', 'Iraq', 'IRQ'),
            ('Iran', 'Iran', 'IRN'),
            ('Indonesia', 'Indonesia', 'IDN'), ('India', 'India', 'IND'), ('Iceland', 'Iceland', 'ISL'),
            ('Hungary', 'Hungary', 'HUN'),
            ('Honduras', 'Honduras', 'HND'), ('Haiti', 'Haiti', 'HTI'), ('Guyana', 'Guyana', 'GUY'),
            ('Guinea-Bissau', 'Guinea-Bissau', 'GNB'),
            ('Guinea', 'Guinea', 'GIN'), ('Guatemala', 'Guatemala', 'GTM'), ('Grenada', 'Grenada', 'GRD'),
            ('Greece', 'Greece', 'GRC'),
            ('Ghana', 'Ghana', 'GHA'), ('Germany', 'Germany', 'DEU'), ('Georgia', 'Georgia', 'GEO'),
            ('Gambia', 'Gambia', 'GMB'),
            ('Gabon', 'Gabon', 'GAB'), ('France', 'France', 'FRA'), ('France', 'Saint Pierre and Miquelon', 'SPM'),
            ('France', 'Wallis and Futuna', 'WLF'),
            ('France', 'Saint Martin', 'MAF'), ('France', 'Saint Barthelemy', 'BLM'),
            ('France', 'French Polynesia', 'PYF'),
            ('France', 'New Caledonia', 'NCL'), ('France', 'French Southern and Antarctic Lands', 'ATF'),
            ('Finland', 'Aland', 'ALD'),
            ('Finland', 'Finland', 'FIN'), ('Fiji', 'Fiji', 'FJI'), ('Ethiopia', 'Ethiopia', 'ETH'),
            ('Estonia', 'Estonia', 'EST'),
            ('Eritrea', 'Eritrea', 'ERI'), ('Equatorial Guinea', 'Equatorial Guinea', 'GNQ'),
            ('El Salvador', 'El Salvador', 'SLV'),
            ('Egypt', 'Egypt', 'EGY'), ('Ecuador', 'Ecuador', 'ECU'),
            ('Dominican Republic', 'Dominican Republic', 'DOM'),
            ('Dominica', 'Dominica', 'DMA'), ('Djibouti', 'Djibouti', 'DJI'), ('Denmark', 'Greenland', 'GRL'),
            ('Denmark', 'Faroe Islands', 'FRO'), ('Denmark', 'Denmark', 'DNK'), ('Czechia', 'Czechia', 'CZE'),
            ('Northern Cyprus', 'Northern Cyprus', 'CYN'),
            ('Cyprus', 'Cyprus', 'CYP'), ('Cuba', 'Cuba', 'CUB'), ('Croatia', 'Croatia', 'HRV'),
            ('Ivory Coast', 'Ivory Coast', 'CIV'),
            ('Costa Rica', 'Costa Rica', 'CRI'),
            ('Democratic Republic of the Congo', 'Democratic Republic of the Congo', 'COD'),
            ('Republic of the Congo', 'Republic of the Congo', 'COG'), ('Comoros', 'Comoros', 'COM'),
            ('Colombia', 'Colombia', 'COL'),
            ('China', 'China', 'CHN'), ('China', 'Macao S.A.R', 'MAC'), ('China', 'Hong Kong S.A.R.', 'HKG'),
            ('Chile', 'Chile', 'CHL'),
            ('Chad', 'Chad', 'TCD'), ('Central African Republic', 'Central African Republic', 'CAF'),
            ('Cabo Verde', 'Cabo Verde', 'CPV'),
            ('Canada', 'Canada', 'CAN'), ('Cameroon', 'Cameroon', 'CMR'), ('Cambodia', 'Cambodia', 'KHM'),
            ('Myanmar', 'Myanmar', 'MMR'),
            ('Burundi', 'Burundi', 'BDI'), ('Burkina Faso', 'Burkina Faso', 'BFA'), ('Bulgaria', 'Bulgaria', 'BGR'),
            ('Brunei', 'Brunei', 'BRN'), ('Brazil', 'Brazil', 'BRA'), ('Botswana', 'Botswana', 'BWA'),
            ('Bosnia and Herzegovina', 'Bosnia and Herzegovina', 'BIH'), ('Bolivia', 'Bolivia', 'BOL'),
            ('Bhutan', 'Bhutan', 'BTN'), ('Benin', 'Benin', 'BEN'), ('Belize', 'Belize', 'BLZ'),
            ('Belgium', 'Belgium', 'BEL'),
            ('Belarus', 'Belarus', 'BLR'), ('Barbados', 'Barbados', 'BRB'), ('Bangladesh', 'Bangladesh', 'BGD'),
            ('Bahrain', 'Bahrain', 'BHR'),
            ('The Bahamas', 'The Bahamas', 'BHS'), ('Azerbaijan', 'Azerbaijan', 'AZE'), ('Austria', 'Austria', 'AUT'),
            ('Australia', 'Australia', 'AUS'), ('Australia', 'Indian Ocean Territories', 'IOA'),
            ('Australia', 'Heard Island and McDonald Islands', 'HMD'),
            ('Australia', 'Norfolk Island', 'NFK'), ('Australia', 'Ashmore and Cartier Islands', 'ATC'),
            ('Armenia', 'Armenia', 'ARM'),
            ('Argentina', 'Argentina', 'ARG'), ('Antigua and Barbuda', 'Antigua and Barbuda', 'ATG'),
            ('Angola', 'Angola', 'AGO'),
            ('Andorra', 'Andorra', 'AND'), ('Algeria', 'Algeria', 'DZA'), ('Albania', 'Albania', 'ALB'),
            ('Afghanistan', 'Afghanistan', 'AFG'),
            ('Kashmir', 'Siachen Glacier', 'KAS'), ('Antarctica', 'Antarctica', 'ATA'),
            ('Netherlands', 'Sint Maarten', 'SXM')]


def draw_map_from_shapefile_and_return_extreme_points(
        ax, shapefile_path, coordinates_system,
        country=None, mask=False, color_to_be_transparent=None,
):
    """Draw map contours from the given shapefile"""
    import shapefile as shp
    from pyproj import Transformer

    shape = shp.Reader(shapefile_path)
    shape = shape.shapes()
    transformer = Transformer.from_crs(coordinates_system, 'epsg:4326', always_xy=True)

    if country is not None:
        new_shape = []
        countries = get_countries_list_for_default_shape()

        if country == 'EUROPE':
            country = [
                'PRT', 'ESP', 'GBR', 'FRA', 'DEU', 'POL', 'CZE',
                'BEL', 'NLD', 'LUX', 'AND', 'CHE', 'ITA', 'AUT', 'SVN',
                'HRV', 'BIH', 'MNE', 'ALB', 'GRC', 'TUR', 'CYP', 'CYN',
                'MLT', 'SMR', 'BGR', 'MKD', 'KOS', 'SRB', 'HUN', 'SVK',
                'UKR', 'ROU', 'BLR', 'MDA', 'RUS', 'LVA', 'LTU', 'EST',
                'FIN', 'SWE', 'NOR', 'DNK', 'GEO', 'FRO', 'ISL', 'MAR',
                'DZA', 'TUN', 'LBY', 'EGY', 'ISR', 'PSX', 'LBN', 'SYR',
                'JOR', 'SAU', 'IRQ', 'IRN', 'ARM'
            ]
            ax.set_ylim(30, 73)
            ax.set_xlim(-25, 45)

        if isinstance(country, str):
            for i, country_name in enumerate(countries):
                if len(country) == 3:
                    if country.upper() == country_name[2]:
                        new_shape.append(shape[i])
                else:
                    for element in country_name[:2]:
                        if country.upper() in element.upper():
                            new_shape.append(shape[i])

        if isinstance(country, list):
            for i, country_name in enumerate(countries):
                for single_country in country:
                    if len(single_country) == 3:
                        if single_country.upper() == country_name[2]:
                            new_shape.append(shape[i])
                    else:
                        for element in country_name[:2]:
                            if single_country.upper() in element.upper():
                                new_shape.append(shape[i])

        shape = new_shape

    all_xs = []
    all_ys = []

    starting_point = None
    for element in shape:
        x_for_plotting = []
        y_for_plotting = []
        for coords in element.points:

            x = coords[0]
            y = coords[1]
            x, y = transformer.transform(x, y)

            x_for_plotting.append(x)
            y_for_plotting.append(y)

            if starting_point is None:
                starting_point = (x, y)
                continue

            if starting_point == (x, y):

                ax.plot(x_for_plotting, y_for_plotting, color='black', lw=1)
                if mask:
                    ax.fill(x_for_plotting, y_for_plotting, color=color_to_be_transparent)

                for i, x_ in enumerate(x_for_plotting):
                    all_xs.append(x_)
                    all_ys.append(y_for_plotting[i])

                x_for_plotting.clear()
                y_for_plotting.clear()
                starting_point = None

        ax.plot(x_for_plotting, y_for_plotting, color='black', lw=1)
        if mask:
            ax.fill(x_for_plotting, y_for_plotting, color=color_to_be_transparent)

        for x_ in x_for_plotting:
            all_xs.append(x_)

        for y_ in y_for_plotting:
            all_ys.append(y_)

    the_low_x = min(all_xs)
    the_high_x = max(all_xs)
    the_low_y = min(all_ys)
    the_high_y = max(all_ys)

    return the_low_x, the_high_x, the_low_y, the_high_y
