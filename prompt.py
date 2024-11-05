import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage
from azure.ai.inference.models import UserMessage
from azure.core.credentials import AzureKeyCredential

# Read content from all files in the requirements directory
requirements_dir = "requirements"
for filename in os.listdir(requirements_dir):
    filepath = os.path.join(requirements_dir, filename)
    if os.path.isfile(filepath):
        with open(filepath, 'r') as file:
            requirements_content = file.read()

        print(f"Requirements content read from {filename}:")
        print(requirements_content)

        # To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings. 
        # Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
        client = ChatCompletionsClient(
            endpoint="https://models.inference.ai.azure.com",
            credential=AzureKeyCredential(os.environ["GITHUB_TOKEN"]),
        )

        response = client.complete(
            messages=[
                SystemMessage(content=""""""),
                UserMessage(content="based on attached context write a XSLT file to fulfill requirements. Here is a sample [attach sample]. Please limit your response to just the XSLT code output." + requirements_content),
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
        with open(output_file_path, "w") as output_file:
            output_file.write(response.choices[0].message.content)