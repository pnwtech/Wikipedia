# Wikipedia Wrapper

## Description

This project is a wrapper API around the Wikipedia API that provides users with the ability to view daily, weekly, and monthly page views for any given Wikipedia page.

## Getting Started

To get started with this API, you will need to first clone the repository to your local machine. You can do this by running the following command in your terminal:

```bash
git clone https://github.com/dperconti/grow.git
```

Once you have cloned the repository, you will need to install the required dependencies. It is recommended to use some form of virtual environment for your dependencies. You can do this by running the following command in the terminal:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Note on Chalice

[Chalice](https://github.com/aws/chalice) is a framework for writing serverless apps in python. It allows you to quickly create and deploy applications that use AWS Lambda. It provides:

- A command line tool for creating, deploying, and managing your app
- A decorator based API for integrating with Amazon API Gateway, Amazon S3, Amazon SNS, Amazon SQS, and other AWS services.
- Automatic IAM policy generation

Chalice was choosen for this project for its simplicity and ease with creating, running, and maintaining API infrastructure.

## Running Locally

```bash
chalice local
```

## Postman Requests

This API is documented with examples using Postman. The Postman requests can be imported from [./docs/postman/Grow.postman_collection.json](./docs/postman/Grow.postman_collection.json)

- [Importing data](https://learning.postman.com/docs/getting-started/importing-and-exporting-data/#importing-postman-data)
- [Running the collection as a whole (which also runs tests)](https://learning.postman.com/docs/running-collections/running-collections-overview/)

## Requirements

● Retrieve a list of the most viewed articles for a week __Included in the `/top` API__
● Retrieve a list of the most viewed articles for a month __Included in the `/top` API__
● For any given article, be able to get the view count of that specific article for a week: __Included in the `/top/{article}` API__
● For any given article, be able to get the view count of that specific article for a month: __Included in the `/top/{article}` API__
● Retrieve the day of the month where an article got the most page views: __Included in the `/top/{article}` API__

## Tests

Tests are currently black box tests only which are included in the Postman collection.
