Dynamic Resource Allocation Across Accounts Using Centralized Cost Monitoring


Problem: For organizations using multiple AWS accounts, managing cloud budgets while dynamically provisioning resources can be challenging, especially when certain accounts might require cost rebalancing.

Solution: Build a system that dynamically adjusts resource provisioning based on the budget of different accounts within an AWS organization. Integrate AWS Budgets, Cost Explorer, and Cloudformation to monitor real-time costs in each account and reassign workloads accordingly.


* Create Cloudformation Infrastructure for Resource Provisioning
* Creating control tower landing zone and deploying the infrastructure in multi account.
* AWS Budgets and Cost Explorer are used to monitor resource usage and costs in each account.
* Cloudformation scripts query these services using Lambda functions to get real-time data on account-level spend.
* Based on predefined thresholds, if an account exceeds a certain cost limit, Cloudformation dynamically re-allocates certain workloads or resources (like EC2 instances) to a cheaper or under-utilized account within the same organization.


Implementation Example:
Use Cloudformation to deploy a Lambda function that checks the AWS Budget for each account and compares the current cost with a limit.
Based on the current usage, use lambda function to scale down resources in the high-cost account and trigger cross-account deployment to a cheaper account using cross-account IAM roles.

Prerequisites

* Multiple AWS accounts configured in AWS Organizations. (Control tower)
* S3 bucket for storing Cloudformation state across accounts.
* IAM roles set up for cross-account access.
* AWS Cost Explorer and Budgets enabled.


Architecture Diagram:



<img width="989" alt="Screenshot 2024-10-09 at 6 06 13 PM" src="https://github.com/user-attachments/assets/7939e1bd-fad3-4b98-aa22-6cf688c99b4b">

Target technology stack:

* AWS CloudFormation
* AWS CodePipeline
* AWS Lambda
* AWS S3
* AWS Control Tower

