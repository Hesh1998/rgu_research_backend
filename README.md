rgu_research_backend-main is the source code from main GIT branch of rgu_research_backend repository hosted on GitHub

GitHub link - https://github.com/Hesh1998/rgu_research_backend.git
* This is the codebase for the Backend of the Web Application which was hosted on AWS Cloud.
* To run this code please follow below steps,
- Save the Databricks Access token as rgu/research/databricks on AWS Secrets Manager.
- Save the API key for Anthropic Claude as rgu/research/claude on AWS Secrets Manager.
- Save the API key for Google Gemini as rgu/research/gemini on AWS Secrets Manager.
- Save the API key for OpenAI GPT as rgu/research/openai on AWS Secrets Manager.
- Create a t3.micro AWS EC2 Instance and Clone the GitHub repository.
- Install Dependencies in AWS EC2 Instance: python3, python3-pip, flask, flask-cors, boto3, botocore, openai, databricks-sql-connector, google-genai, anthropic, aws
- Create a user with full Administrator Access as aws-cli-user on AWS IAM Users.
- Use aws configure to configure the Admin user on AWS EC2.
- Run app.py script using python3 command.
