import argparse
import boto3
import time
import uuid


def get_distribution_id(domain):
    # Function to get the CloudFront distribution ID based on the domain
    cloudfront_client = boto3.client('cloudfront')

    # Retrieve a list of CloudFront distributions
    response = cloudfront_client.list_distributions()

    # Check each distribution for matching aliases
    for distribution in response['DistributionList']['Items']:
        aliases = distribution['Aliases']['Items']
        if domain in aliases:
            return distribution['Id']

    return None


def clear_cloudfront_cache(distribution_id, paths, domain):
    # Function to clear the CloudFront cache for specified distribution and paths
    cloudfront_client = boto3.client('cloudfront')

    # Output domain and path information
    print(f'Distribution ID: {distribution_id} ({domain})')
    print(f'URL Path: {", ".join(paths)}')

    # Prompt for confirmation to clear the cache for the specified distribution and paths
    confirmation = input(
        '**Are you sure you want to clear the CloudFront cache for the above distribution and paths? (y/n): ')

    if confirmation.lower() == 'y':
        # If confirmed, combine all paths into one invalidation batch
        invalidation_paths = list(paths)

        # Generate a unique CallerReference using a combination of timestamp and UUID
        caller_reference = f'script-triggered-invalidation-{int(time.time())}-{uuid.uuid4()}'

        response = cloudfront_client.create_invalidation(
            DistributionId=distribution_id,
            InvalidationBatch={
                'Paths': {
                    'Quantity': len(invalidation_paths),
                    'Items': invalidation_paths
                },
                'CallerReference': caller_reference
            }
        )

        for path in invalidation_paths:
            print(f'Cache invalidation initiated for path {path}: Invalidation ID: {response["Invalidation"]["Id"]}')
    else:
        # If not confirmed, skip cache invalidation
        print('--Skipped.')


def main():
    # Main function to parse command-line arguments and execute cache invalidation
    parser = argparse.ArgumentParser(description='Clear CloudFront cache based on URL and AWS SSO authentication.')
    parser.add_argument('--urls', nargs='+', required=True,
                        help='Multiple URLs for which the CloudFront cache should be cleared.')

    args = parser.parse_args()

    # Extracting domains and paths from the URLs
    distributions = {}

    for url in args.urls:
        domain = url.split('//')[1].split('/')[0] if '//' in url else url.split('/')[0]
        path_parts = url.split('/')[1:]
        path = '/' + '/'.join(path_parts)

        # Get the distribution ID for each domain
        distribution_id = get_distribution_id(domain)

        if distribution_id:
            if distribution_id not in distributions:
                distributions[distribution_id] = {
                    'domain': domain,
                    'paths': {path},
                }
            else:
                distributions[distribution_id]['paths'].add(path)
        else:
            print(f'No CloudFront distribution found for the provided domain: {domain}')

    # Iterate through each distribution and initiate cache invalidation
    for distribution_id, data in distributions.items():
        clear_cloudfront_cache(distribution_id, data['paths'], data['domain'])


if __name__ == "__main__":
    main()
