import argparse
import logging
import csv
import time

import coloredlogs
import googlemaps


logger = logging.getLogger(__name__)


def main(csv_input_file, input_column, api_key, csv_output_file):
    logger.info('Starting Google Maps client with API Key %s', api_key)
    gmaps = googlemaps.Client(key=api_key)

    with open(csv_input_file, newline='') as csv_input_file_obj, open(csv_output_file, 'w', newline='') as csv_output_file_obj:
        reader = csv.reader(csv_input_file_obj, delimiter=',')
        writer = csv.writer(csv_output_file_obj, delimiter=',')
        is_first_row = True
        for row in reader:
            logger.info('%s', row)
            if is_first_row:
                logger.info('First Row')
                is_first_row = False
                row.append('formatted_address')
                row.append('lat')
                row.append('lng')
            else:
                geocode_results = []
                try:
                    # See https://developers.google.com/maps/documentation/geocoding/intro#GeocodingResponses
                    geocode_results = gmaps.geocode(row[input_column])
                    logger.info('%s', geocode_results)
                except googlemaps.exceptions.HTTPError as e:
                    logger.error('Failed with %s', e)
                if len(geocode_results) == 0:
                    logger.warning('Not results found')
                    row.append('')
                    row.append('')
                    row.append('')
                else:
                    geocode_result = geocode_results[0]
                    row.append(geocode_result['formatted_address'])
                    row.append(geocode_result['geometry']['location']['lat'])
                    row.append(geocode_result['geometry']['location']['lng'])

            writer.writerow(row)
            time.sleep(0.2)


    print(geocode_result)

if __name__ == '__main__':
    coloredlogs.install(level='INFO')

    parser = argparse.ArgumentParser(description='Append location to CSV.')
    parser.add_argument('csv_input_file', metavar='FILE', type=str, help='The CSV file of data')
    parser.add_argument('input_column', metavar='COLUMN', type=int, help='The column number (0 indexed)')
    parser.add_argument('api_key', metavar='API_KEY', type=str, help='Your Google Maps API key')
    parser.add_argument('csv_output_file', metavar='FILE', type=str, help='The CSV file of data')

    args = parser.parse_args()
    main(args.csv_input_file, args.input_column, args.api_key, args.csv_output_file)