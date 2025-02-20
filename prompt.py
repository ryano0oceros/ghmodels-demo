import os
import time
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage
from azure.ai.inference.models import UserMessage
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import ServiceRequestError, ServiceResponseError, HttpResponseError

# Read static content from prompt.txt in the root directory
with open("prompt.txt", 'r', encoding='utf-8', errors='ignore') as file:
    static_content = file.read()

# Read content from all files in the requirements directory
requirements_dir = "requirements"
for filename in os.listdir(requirements_dir):
    filepath = os.path.join(requirements_dir, filename)
    if os.path.isfile(filepath):
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            requirements_content = file.read()

        # Create a variable full_prompt by joining static_content and requirements_content
        full_prompt = static_content + "\n" + requirements_content

        # To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings. 
        # Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
        client = ChatCompletionsClient(
            endpoint=os.getenv("AZURE_ENDPOINT"),
            credential=AzureKeyCredential(os.getenv("AZURE_KEY")),
        )

        # Test authentication against the endpoint
        try:
            test_response = client.complete(
                messages=[
                    SystemMessage(content="Test authentication message"),
                ],
                model="gpt-4o",
                temperature=1,
                max_tokens=10,
                top_p=1
            )
        except Exception as e:
            continue

        # Retry mechanism with exponential backoff
        max_retries = 5
        retry_delay = 1  # Initial delay in seconds

        for attempt in range(max_retries):
            try:
                response = client.complete(
                    messages=[
                        SystemMessage(content=""""""),
                        UserMessage(content=full_prompt),
                    ],
                    model="gpt-4o",
                    temperature=1,
                    max_tokens=4096,
                    top_p=1
                )
                print(f"Response from the model for {filename}:")
                print(response.choices[0].message.content)

                # Write the response to a file named after the original file with _response.txt appended
                base_filename = os.path.splitext(filename)[0]
                output_file_path = os.path.join("outputs", f"{base_filename}_response.txt")
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                with open(output_file_path, "w", encoding='utf-8') as output_file:
                    output_file.write(response.choices[0].message.content)
                
                # Add a delay between requests
                time.sleep(2)  # Delay for 2 seconds
                break  # Exit the retry loop if the request is successful
            except (ServiceRequestError, ServiceResponseError, HttpResponseError) as e:
                if isinstance(e, HttpResponseError) and e.status_code == 429:
                    retry_delay = int(e.response.headers.get("Retry-After", retry_delay))
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    break

print("Processing completed.")