

def calc_the_distance(
        point1, point2
):
    """Calculate the distance between two given points"""
    import math

    a = abs(point1[0] - point2[0])
    b = abs(point1[1] - point2[1])
    c2 = a**2 + b**2

    c = math.sqrt(c2)

    return c


def get_countries_list_for_default_shape():
    return [
        'Zimbabwe', 'Zambia', 'Yemen', 'Vietnam', 'Venezuela', 'Vatican', 'Vanuatu', 'Uzbekistan', 'Uruguay',
        'Federated States of Micronesia', 'Marshall Islands', 'United States of America', 'United States of America',
        'United States of America', 'United States of America', 'United States of America', 'United States of America',
        'United Kingdom', 'United Kingdom', 'United Kingdom', 'United Kingdom', 'United Kingdom', 'United Kingdom',
        'United Kingdom', 'United Kingdom', 'United Kingdom', 'United Kingdom', 'United Kingdom', 'United Kingdom',
        'United Kingdom', 'United Kingdom', 'United Kingdom', 'United Arab Emirates', 'Ukraine', 'Uganda', 'Turkmenistan',
        'Turkey', 'Tunisia', 'Trinidad and Tobago', 'Tonga', 'Togo', 'East Timor', 'Thailand', 'United Republic of Tanzania',
        'Tajikistan', 'Taiwan', 'Syria', 'Switzerland', 'Sweden', 'Swaziland', 'Suriname', 'South Sudan', 'Sudan', 'Sri Lanka',
        'Spain', 'South Korea', 'South Africa', 'Somalia', 'Somaliland', 'Solomon Islands', 'Slovakia', 'Slovenia', 'Singapore',
        'Sierra Leone', 'Seychelles', 'Republic of Serbia', 'Senegal', 'Saudi Arabia', 'São Tomé and Principe', 'San Marino',
        'Samoa', 'Saint Vincent and the Grenadines', 'Saint Lucia', 'Saint Kitts and Nevis', 'Rwanda', 'Russia', 'Romania',
        'Qatar', 'Portugal', 'Poland', 'Philippines', 'Peru', 'Paraguay', 'Papua New Guinea', 'Panama', 'Palau', 'Pakistan',
        'Oman', 'Norway', 'North Korea', 'Nigeria', 'Niger', 'Nicaragua', 'New Zealand', 'New Zealand', 'New Zealand',
        'Netherlands', 'Netherlands', 'Netherlands', 'Nepal', 'Nauru', 'Namibia', 'Mozambique', 'Morocco', 'Western Sahara',
        'Montenegro', 'Mongolia', 'Moldova', 'Monaco', 'Mexico', 'Mauritius', 'Mauritania', 'Malta', 'Mali', 'Maldives',
        'Malaysia', 'Malawi', 'Madagascar', 'North Macedonia', 'Luxembourg', 'Lithuania', 'Liechtenstein', 'Libya', 'Liberia',
        'Lesotho', 'Lebanon', 'Latvia', 'Laos', 'Kyrgyzstan', 'Kuwait', 'Kosovo', 'Kiribati', 'Kenya', 'Kazakhstan', 'Jordan',
        'Japan', 'Jamaica', 'Italy', 'Israel', 'Israel', 'Ireland', 'Iraq', 'Iran', 'Indonesia', 'India', 'Iceland', 'Hungary',
        'Honduras', 'Haiti', 'Guyana', 'Guinea-Bissau', 'Guinea', 'Guatemala', 'Grenada', 'Greece', 'Ghana', 'Germany',
        'Georgia', 'Gambia', 'Gabon', 'France', 'France', 'France', 'France', 'France', 'France', 'France', 'France',
        'Finland', 'Finland', 'Fiji', 'Ethiopia', 'Estonia', 'Eritrea', 'Equatorial Guinea', 'El Salvador', 'Egypt',
        'Ecuador', 'Dominican Republic', 'Dominica', 'Djibouti', 'Denmark', 'Denmark', 'Denmark', 'Czechia', 'Northern Cyprus',
        'Cyprus', 'Cuba', 'Croatia', 'Ivory Coast', 'Costa Rica', 'Democratic Republic of the Congo', 'Republic of the Congo',
        'Comoros', 'Colombia', 'China', 'China', 'China', 'Chile', 'Chad', 'Central African Republic', 'Cabo Verde', 'Canada',
        'Cameroon', 'Cambodia', 'Myanmar', 'Burundi', 'Burkina Faso', 'Bulgaria', 'Brunei', 'Brazil', 'Botswana',
        'Bosnia and Herzegovina', 'Bolivia', 'Bhutan', 'Benin', 'Belize', 'Belgium', 'Belarus', 'Barbados', 'Bangladesh',
        'Bahrain', 'The Bahamas', 'Azerbaijan', 'Austria', 'Australia', 'Australia', 'Australia', 'Australia', 'Australia',
        'Armenia', 'Argentina', 'Antigua and Barbuda', 'Angola', 'Andorra', 'Algeria', 'Albania', 'Afghanistan', 'Kashmir',
        'Antarctica', 'Netherlands']


def draw_map_from_shapefile_and_return_extreme_points(
        ax, shapefile_path, coordinates_system,
        country=None, mask=False, color_to_be_transparent=None
):
    """Draw map contours from the given shapefile"""
    import shapefile as shp
    from pyproj import Transformer

    shape = shp.Reader(shapefile_path)
    shape = shape.shapes()
    transformer = Transformer.from_crs(coordinates_system, 'epsg:4326')

    if country is not None:
        new_shape = []
        country_names = get_countries_list_for_default_shape()

        for i, country_name in enumerate(country_names):
            if country.upper() in country_name.upper():
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
