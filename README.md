# CloudFront Cache Clear Script

## Overview

This script is designed to clear the CloudFront cache for specified URLs based on AWS SSO authentication. It groups URLs by CloudFront distribution and initiates cache invalidation for each distribution.

## Prerequisites

- dependency library installed 
  - ```bash
      pip install -r requirements.txt
      ```
- AWS CLI configured with the necessary credentials (SSO)

## Usage

1. Clone this repository or download the script.
2. Install the required Python packages:

    ```bash
    pip3 install boto3
    ```

3. Run the script with the desired URLs: (make sure to enter url without https://)

    ```bash
    python3 cloudfront_cache_clear.py --url 'example1.com/path1/dsa/dsa.js'  'example1.com/path2/ddsa/*' 'example2.com/path1/*' ...
    ```

4. Follow the prompts to confirm cache invalidation for each distribution.

## Script Details

- **`cloudfront_cache_clear.py`**: Main Python script.
- **`get_distribution_id(domain)`**: Function to get the CloudFront distribution ID based on the domain.
- **`clear_cloudfront_cache(distribution_id, paths, domain)`**: Function to clear the CloudFront cache for a specified distribution and paths.
- **`main()`**: Main function to parse command-line arguments and execute cache invalidation.

## Important Note

Ensure that the AWS CLI is properly configured with the necessary credentials. The script uses Boto3, the AWS SDK for Python, to interact with AWS services.
