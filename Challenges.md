### Challenge 1: Threads, Marshmallow, and Socket

Threaded Port Scanner (Python Fundamentals + Security + Data Validation)

Task:
Implement a multi-threaded TCP port scanner in Python. Your program should:

1. Accept a target host (IP address or domain name) and a range of ports to scan.

2. Use threads to scan multiple ports concurrently.

3. Report which ports are open and which are closed.

4. Handle errors gracefully (e.g., invalid input, unreachable host).

5. Use Marshmallow for input validation and serialization:

6. Define a schema that validates the scan request (host, start_port, end_port, thread_count).

7. Ensure invalid inputs (e.g., negative ports, non-integers, malformed hostnames) are rejected before the scan starts.

8. Serialize the results into a JSON-like structure (a dictionary dump via Marshmallow) for output.

Additional Details:

Use the socket module for scanning.

Use threading.Thread (or concurrent.futures.ThreadPoolExecutor) for concurrency.

The Marshmallow schema should be the first step — i.e., input is validated and converted into a Python object before any scanning occurs.

For bonus points, implement a @post_load method in Marshmallow to automatically construct a ScanRequest object from validated input.