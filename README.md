# Scaling with External APIs & Vendors

Scaling a SaaS product that relies on external APIs and vendors can be complex, but it's essential for ensuring seamless functionality and user satisfaction. This blog will explore key considerations and best practices for scaling SaaS products that integrate with third-party and external APIs and vendors. In addition, we'll cover topics such as fallback logic, performance optimization, API management, and vendor management.

## Preface

To illustrate, we will use the [Wikimedia API](https://wikitech.wikimedia.org/wiki/Analytics/AQS/Pageviews) to fetch page view counts for a specified period. This scenario can include integration with third-party banks, e-commerce providers, movie review sites, and more. The implementation will be divided into several requirements, including obtaining the top monthly, weekly, and daily views and views within specific date ranges.

1. Get Top Monthly Views
2. Get Top Weekly Views
3. Get Top Daily Views
4. Get Top Views Between Dates

We'll look at three different time frames for obtaining this information.

- Monthly - This is a pre-existing API provided by Wikimedia by using all-days
- Weekly - This is **not** a pre-existing API provided by Wikimedia, so we'll need to query the daily endpoints and aggregate based on the given week.
- Daily - This is a pre-existing API provided by Wikimedia.

## Tools

**[LocalStack](https://localstack.cloud/)**
This blog will focus mainly on architectural strategies and implementation for segregating concerns and priorities of different services. LocalStack provides a means to implement these strategies and preview the resulting improvements locally.

**[Chalice](https://github.com/aws/chalice)**
Chalice is a Python-based serverless microframework designed for use with AWS. Using this tool, we can quickly create streamlined APIs, serverless functions, a DynamoDB instance, and an SQS queue.

## Getting started

To get started with this API, you must clone the repository to your local machine. You can do this by running the following command in your terminal:

```bash
git clone https://github.com/pnw.tech/grow.git
```

Once you have cloned the repository, you must install the required dependencies. Again, using some form of a virtual environment for your dependencies is recommended. You can do this by running the following command in the terminal:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

From here, there is a python script in the root directory that can be run with the following:

```bash
python init.py
```

This will do the following:
Create a DynamoDB local instance based on `dynamodb/config.json`
Create an SQS queue
Deploy the growth API (API Gateway & serverless lambda)
Deploy the ingestion API (serverless lambda that will listen to the SQS queue)

## Strategy

Now that we have the working example at our fingertips let's dive into the implementation strategy.

## Parallelizing & Batching

Parallelizing and batching API calls are two techniques commonly used to optimize the performance of API-driven applications.

Parallelizing API calls involves sending multiple requests simultaneously instead of waiting for one request to finish before sending the next one. This can lead to faster response times and increased throughput, especially in scenarios where many API calls need to be made. Parallelization can be implemented using multithreading, multiprocessing, or asynchronous programming models.

In our particular example, for the weekly top views request, we know that we will *always* need to request seven separate resources (each day to aggregate for the weekly top views). So, instead of waiting for each request to complete, let's parallelize these requests!

Seen in [period.py](https://github.com/pnwtech/Wikipedia/blob/55b6ac20a1612193a099c812e8459fe1210640db/chalicelib/wikipedia/period.py#L73-L76):

```python
    with futures.ThreadPoolExecutor(max_workers=7) as executor:
        res = executor.map(__unravel_top_request__, request_object)
    response_object = list(res)
```

Batching API calls involves grouping multiple API requests into one request, which can be sent to the server in one go. This reduces the number of round trips between the client and server, which can help reduce latency and improve network efficiency. Batching can be implemented using custom code or third-party libraries or services providing batching capabilities. In our case, we can do this for the monthly request but not for weekly or other days that aren't a month.

Advantages of parallelizing and batching API calls include:
Improved performance and reduced latency: By sending multiple requests simultaneously or grouping various requests into a single request, parallelizing and batching can help reduce response times and improve overall performance.

- Increased throughput: Parallelizing and batching can increase the number of API calls made per unit of time, which is especially useful in high-load scenarios.
- Reduced network overhead: By reducing the number of round trips between the client and server, parallelizing and batching can help reduce network overhead and improve network efficiency.

However, there are also some disadvantages to consider when using these techniques:

- Increased complexity: Parallelizing and batching can introduce additional complexity into an application, especially when dealing with errors and retries.
- Increased resource usage: Parallelizing and batching can consume more system resources, especially when dealing with extensive data or high-concurrency scenarios.
- Limited compatibility: Only some APIs support parallelization or batching, so these techniques may only be applicable in some scenarios, and you may run into rate limits.

Determining the optimal batch size for a given use case can depend on network latency, API response times, and available system resources. In general, smaller batch sizes may be more appropriate for scenarios with high network latency or high variability in API response times. Comparatively, larger batch sizes may be more suitable for scenarios with low network latency or high system resources.

## Direct vs Local

One of the most common challenges when handling vendor data is determining the most effective way to access and store this information. As a developer or engineer, it's crucial to weigh the pros and cons of each approach to ensure that your system operates efficiently and accurately. The two primary options are to either store a local copy of the vendor's data or to obtain and pass through the information as needed directly.

If you're starting, opting for a direct pass-through approach is generally recommended. This means that whenever a user requests data from your system, your system sends a request to the vendor's API, retrieves the necessary data, and passes it back to the user. This method avoids storing a local copy of the vendor's data and ensures the user receives the most up-to-date information. However, as you scale up and handle more requests, relying solely on direct pass-through can lead to performance issues, as it can cause excessive API requests that can slow down the system.

On the other hand, storing a local copy of the vendor's data can offer several benefits. Firstly, it can reduce the number of API requests, improving the system's performance. Secondly, if the vendor's API experiences downtime or is otherwise unavailable, having a local copy of the data can ensure your system can continue operating without interruption. However, there are also several downsides to this approach. Storing a copy of the vendor's data can lead to inconsistencies and outdated information if not properly maintained. Additionally, adding or modifying data can become challenging and require manual intervention to ensure that both the local copy and the vendor's data are aligned and accurate.

Given these considerations, balancing the two approaches that work best for your specific use case is essential. A general rule of thumb is to keep the vendor's record as the source of truth and use local storage only when the vendor's data is unavailable. This way, you can ensure that your system always uses the most up-to-date and accurate data. However, the ultimate decision should depend on the end-users needs and the specific requirements of your product.

For instance, if you're dealing with historical data that is unlikely to change frequently, storing a local copy may make more sense to reduce API request time. This approach could benefit applications requiring rapid but older data access, such as historical analytics. In contrast, if your end-users require real-time and frequently updated information, relying solely on the vendor's data may be best and using local storage only as a backup.

One potential solution to local storage challenges is to implement a messaging queue that allows requests to be processed during peak periods or when a large number of requests need to be handled by the downstream lambda. The downstream lambda ingests the queue, storing the information in a key/value format using a database like DynamoDB. This approach ensures that requests are not blocked while data is stored locally. Additionally, an in-memory database like Redis could be considered if high-performance scenarios are necessary. It offers fast read and write speeds and can handle large amounts of data.

In our case, the data is historical data. Therefore, view counts of March 20th, 2022, will remain the same if I query today versus tomorrow. Because of this, I would look at storing these records locally, especially if I want to reduce API request time. To do this, I've implemented the strategy:

1. Prefer local storage.
2. If the local storage does not contain the requested records, we'll obtain them through Wikimedia.
3. Once we have the data, let's store it but not block the original request.
4. To do this without blocking, I've implemented a messaging queue to further allow requests during spike periods or large amounts of requests that need to be handled by the downstream lambda. The downstream lambda will ingest the queue and store the information in a key/value format with DynamoDB.

![alt text](images/FigJam.jpg "Architecture Image")

## Handling Timeouts & Rate Limiting

When interacting with external APIs, timeouts and rate limiting are essential considerations. Timeouts occur when a request to an API takes longer than expected to return a response. This can happen for various reasons, such as network latency or the API being overloaded with requests. Rate limiting occurs when an API provider limits the number of requests that can be made within a specific timeframe. This is done to prevent abuse of the API and ensure fair usage by all consumers.

To handle timeouts and rate limiting when interacting with external APIs, there are a few best practices that you can follow.

- Set reasonable timeouts: It's essential to set appropriate timeouts for API requests, so your application doesn't hang indefinitely waiting for a response. Depending on the API and the use case, timeouts can be set anywhere from a few seconds to a few minutes.
- Implement retry logic: In case of a timeout or rate limiting, retrying the request after a short delay can be an excellent strategy to handle the issue. However, it's vital to implement retry logic carefully to avoid creating more load on the API and potentially exacerbating the problem.
- Monitor API usage: Monitoring your API usage can help you identify when you're approaching rate limits or experiencing frequent timeouts. This can allow you to take proactive measures to reduce API load or increase your capacity if needed.

## Summary

Several strategies can be used to scale with external APIs and vendors, including handling timeouts and rate limiting, directly or indirectly accessing vendor data and parallelizing and batching requests.

Handling timeouts and rate limiting involves setting reasonable timeouts, implementing retry logic, monitoring API usage, using caching, and considering parallelization. Using these techniques, an application can be more resilient to issues such as network latency and API overload, reducing the likelihood of exceeding rate limits.

Directly or indirectly accessing vendor data involves choosing whether to store a local copy of the data or to retrieve it directly from the vendor. When starting, it's best to prefer a direct pass-through to the vendor's data. However, as an application scales up, having a local copy and direct access to the vendor's data may be beneficial as a form of redundancy.

Parallelizing and batching requests involve sending multiple requests simultaneously or combining various requests into a single batch request. Using these techniques, an application can reduce the time it takes to retrieve data and reduce the likelihood of timeouts. However, it's crucial to balance the benefits of parallelization and batching against the potential impact on the API and any rate limits that are in place.

Using these strategies, an application can scale more effectively with external APIs and vendors, providing a better experience for end-users. However, it's essential to consider the API provider's specific requirements and guidance and implement these strategies carefully to avoid causing issues or exceeding rate limits.
