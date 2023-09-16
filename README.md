# Prompt-LLM Translator 🌟🚀

A Gradio Chat App for a LLM assisted Translator

## Installation

Dependencies:
- [Python](https://www.python.org/)

Install the Python dependencies using the following commands:
```bash
python -m pip install virtualenv
python -m venv venv
```
If you are using windows:
```bash
venv\Scripts\activate
```
On linux-based systems:
```bash
source venv/bin/activate
```
Install the requirements:
```bash
python -m pip install -r requirements.txt
```
Install for development:
```bash
python -m pip install -e .
```

### Set up your Local Environment

Copy and rename [`.env.template`](.env.template) to `.env`:
```bash
cp .env.template .env
```
Insert your secrets and other configuration in the [`.env`](.env) file.



## Usage

### Manual Usage

You can start the gradio app manually with the following commands:
```bash
# Use the file
python src/gradio_chat/app.py
# Use the command
gradio-chat
```
It is also possible to use the Pro-LLM Translator individually:
```bash
# Use the file
python src/prollm_translator/main.py
# Use the command
prollm-translator
```

### Docker Compose

You can also use the gradio app with the provided docker compose setup. Just follow the commands below:
```bash
docker compose build
docker compose up
```

### GCP Deployment

#### GCP Artifact Registry

## Manually upload Docker Images (w/ CLI)

1. Provide Docker with priviledged access to interact with registries (follow the [tutorial](../../windows/powershell/README.md))
2. Log out and log back in (let group membership changes to take effect)
3. Load your GCP application credentials
```bash
gcloud auth application-default login
```
2. Set the correct GCP project
```bash
gcloud config set project prollm-translator
```
4. Create a new Docker artifact repository
```bash
# Command:
gcloud artifacts repositories create REPOSITORY_NAME \
    --repository-format=docker \
    --location=REGION \
    --description=DESCRIPTION

# Example:
gcloud artifacts repositories create prollm-translator \
    --repository-format=docker \
    --location=us-central1 \
    --description="Docker repository"
```
1. Verify the artifact repository creation
```bash
gcloud artifacts repositories list
```
1. Configure authentification
```bash
# Command: 
gcloud auth configure-docker REGION-docker.pkg.dev

# Example:
gcloud auth configure-docker us-central1-docker.pkg.dev
```
1. Build a Docker image
```bash
docker build -t prollm-translator .
```
1. Tag the Docker image with the artifact repository name
```bash
# Command:
docker tag prollm-translato \
    REGION-docker.pkg.dev/PROJECT/REPOSITORY_NAME/IMAGE_NAME:TAG

# Example:
docker tag prollm-translator \
    us-central1-docker.pkg.dev/prollm-translator/prollm-translator/prollm-translator:0.0.1
```
8. Push the image to the artifact registry
```bash
# Command:
docker push REGION-docker.pkg.dev/PROJECT/REPOSITORY_NAME/IMAGE_NAME:TAG

# Example:
docker push us-central1-docker.pkg.dev/prollm-translator/prollm-translator/prollm-translator:0.0.1
```
9. Pull the Docker image from the artifact registry
```bash
# Command:
docker pull REGION-docker.pkg.dev/PROJECT/REPOSITORY_NAME/IMAGE_NAME:TAG

# Example:
docker pull us-central1-docker.pkg.dev/prollm-translator/prollm-translator/prollm-translator:0.0.1
```
10. Delete the artifact repository
```bash
# Command:
gcloud artifacts repositories delete REPOSITORY_NAME --location=REGION

# Example:
gcloud artifacts repositories delete prollm-translator --location=us-central1
```

#### Terraform

We provide a terraform configuration for a Prompt-LLM Translator in GCP.

You will need to install the following dependencies:
- gcloud CLI
- Terraform Community Edition

##### Create a GCP Compute Instance Deployment

1. Load your GCP application credentials
```bash
gcloud auth application-default login
```
2. Set the correct GCP project
```bash
gcloud config set project prollm-translator
```
3. [Create a GCP service account key](https://cloud.google.com/iam/docs/keys-create-delete) (see [Terraform tutorial](https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/google-cloud-platform-build#:~:text=A%20GCP%20service%20account%20key%3A%20Create%20a%20service%20account%20key)) and save it the `terraform/key.json` path
4. Generate a new SSH key for this deployment (Note: Remember to safely store your new passphrase!)
```bash
ssh-keygen -f .ssh/id_rsa -N INSERT_YOUR_PASSPHRASE_HERE
```
5. Update your SSH username in the [`.env`](.env) file
6. Initialize the Terraform working directory
```bash
# cd terraform
terraform init
```
7. Generates a speculative Terraform execution plan
```bash
# cd terraform
terraform plan -out tfplan
```
8. Create or update infrastructure according to Terraform configuration
```bash
# cd terraform
terraform apply "tfplan"
```
9. Describe your deployed GCP Compute Instance VM
```bash
gcloud compute instances describe prollm-translator --zone ZONE
```
10. Find the external IP adress of your GCP Compute Instance VM in the description under `networkInterfaces[0].accessConfigs[0].natIP`
11. SSH into your GCP Compute Instance VM
```bash
ssh -i .ssh/id_rsa USERNAME@EXTERNAL_IP
```
12. Destroy Terraform-managed infrastructure
```bash
# cd terraform
terraform destroy
```