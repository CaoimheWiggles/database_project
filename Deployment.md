# Deployment Instructions for My Web App


## Prerequisites
- Render.com account

## Steps to Deploy on Render.com

### Step 1: Sign in to Render.com
Navigate to [Render.com](https://render.com) and sign in to your account.

### Step 2: Create a New Web Service
Go to the Render Dashboard and click on "New" then select "Web Service".

### Step 3: Connect Your Repository
Use my github.com/CaoimheWiggles/database_project to deploy onto Render

### Step 4: Configure the Web Service
- **Name:** database_project
- **Build Command:**  pip install -r requirements.txt
- **Start Command:** gunicorn app:app

### Step 5: Deploy the Web Service
Click on "Create Web Service" to deploy. Wait for the deployment process to complete.
